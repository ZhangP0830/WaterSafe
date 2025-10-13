"""
Test cases for guidance API
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, MagicMock
import json
import time

class TestGuidanceAPI:
    """Test cases for guidance API functionality"""

    def test_guidance_flags_model(self):
        """TC-BE-048: Test guidance flags model validation"""
        from api.guidance import GuidanceFlags
        
        # Test valid flags
        flags = GuidanceFlags(pregnant=True, infant=False)
        assert flags.pregnant is True
        assert flags.infant is False
        
        # Test default values
        flags_default = GuidanceFlags()
        assert flags_default.pregnant is False
        assert flags_default.infant is False

    def test_sanitation_request_model(self, sample_sanitation_request):
        """TC-BE-049: Test sanitation request model validation"""
        from api.guidance import SanitationRequest
        
        # Test valid request
        request = SanitationRequest(**sample_sanitation_request)
        assert request.mode == "general"
        assert request.place == "home"
        assert request.profile.pregnant is True
        assert request.profile.infant is False
        assert "no_running_water" in request.issues

    def test_sanitation_request_invalid_mode(self):
        """TC-BE-050: Test sanitation request with invalid mode"""
        from api.guidance import SanitationRequest
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            SanitationRequest(
                mode="invalid_mode",
                place="home",
                profile={"pregnant": False, "infant": False}
            )

    def test_sanitation_request_invalid_place(self):
        """TC-BE-051: Test sanitation request with invalid place"""
        from api.guidance import SanitationRequest
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            SanitationRequest(
                mode="general",
                place="invalid_place",
                profile={"pregnant": False, "infant": False}
            )

    def test_checklist_source_model(self):
        """TC-BE-052: Test checklist source model"""
        from api.guidance import ChecklistSource
        
        # Test with URL
        source = ChecklistSource(label="WHO", url="https://www.who.int")
        assert source.label == "WHO"
        assert source.url == "https://www.who.int"
        
        # Test without URL
        source_no_url = ChecklistSource(label="Local Health")
        assert source_no_url.label == "Local Health"
        assert source_no_url.url is None

    def test_checklist_item_model(self):
        """TC-BE-053: Test checklist item model"""
        from api.guidance import ChecklistItem, ChecklistSource
        
        item = ChecklistItem(
            id="test-item",
            title="Test Item",
            body="Test description",
            done=False,
            priority="high",
            badges=["Important"],
            icons=["🧼"],
            actions=["Action 1", "Action 2"],
            why="Test reason",
            sources=[ChecklistSource(label="WHO", url="https://www.who.int")]
        )
        
        assert item.id == "test-item"
        assert item.title == "Test Item"
        assert item.priority == "high"
        assert len(item.badges) == 1
        assert len(item.icons) == 1
        assert len(item.actions) == 2

    def test_checklist_section_model(self):
        """TC-BE-054: Test checklist section model"""
        from api.guidance import ChecklistSection, ChecklistItem
        
        item = ChecklistItem(title="Test Item")
        section = ChecklistSection(name="Test Section", items=[item])
        
        assert section.name == "Test Section"
        assert len(section.items) == 1
        assert section.items[0].title == "Test Item"

    def test_checklist_note_model(self):
        """TC-BE-055: Test checklist note model"""
        from api.guidance import ChecklistNote
        
        note = ChecklistNote(type="pregnancy", text="Pregnancy-specific guidance")
        assert note.type == "pregnancy"
        assert note.text == "Pregnancy-specific guidance"

    def test_checklist_response_model(self):
        """TC-BE-056: Test checklist response model"""
        from api.guidance import ChecklistResponse, ChecklistItem, ChecklistSection, ChecklistNote, ChecklistSource
        
        item = ChecklistItem(title="Test Item")
        section = ChecklistSection(name="Test Section", items=[item])
        note = ChecklistNote(type="general", text="General note")
        source = ChecklistSource(label="WHO", url="https://www.who.int")
        
        response = ChecklistResponse(
            summary_top3=[item],
            sections=[section],
            notes=[note],
            sources=[source]
        )
        
        assert len(response.summary_top3) == 1
        assert len(response.sections) == 1
        assert len(response.notes) == 1
        assert len(response.sources) == 1

    def test_generate_context_hash(self):
        """TC-BE-057: Test context hash generation"""
        from api.guidance import _generate_context_hash
        
        context1 = {"mode": "general", "place": "home"}
        context2 = {"mode": "general", "place": "home"}
        context3 = {"mode": "flood", "place": "home"}
        
        hash1 = _generate_context_hash(context1)
        hash2 = _generate_context_hash(context2)
        hash3 = _generate_context_hash(context3)
        
        assert hash1 == hash2  # Same context should produce same hash
        assert hash1 != hash3  # Different context should produce different hash
        assert len(hash1) == 64  # SHA256 hash length

    def test_is_cache_valid(self):
        """TC-BE-058: Test cache validity checking"""
        from api.guidance import _is_cache_valid
        
        # Test valid cache (recent timestamp)
        recent_timestamp = time.time() - 60  # 1 minute ago
        assert _is_cache_valid(recent_timestamp) is True
        
        # Test expired cache (old timestamp)
        old_timestamp = time.time() - (20 * 60)  # 20 minutes ago
        assert _is_cache_valid(old_timestamp) is False

    def test_clean_expired_cache(self):
        """TC-BE-059: Test expired cache cleaning"""
        from api.guidance import _clean_expired_cache, _checklist_cache
        
        # Add some test cache entries
        current_time = time.time()
        _checklist_cache["valid_hash"] = {"data": "test_data", "ts": current_time - 60}
        _checklist_cache["expired_hash"] = {"data": "test_data", "ts": current_time - (20 * 60)}
        
        # Clean expired cache
        _clean_expired_cache()
        
        # Check that expired entry was removed
        assert "valid_hash" in _checklist_cache
        assert "expired_hash" not in _checklist_cache

    def test_rule_based_checklist_general_mode(self):
        """TC-BE-060: Test rule-based checklist for general mode"""
        from api.guidance import _rule_based_checklist, SanitationRequest, GuidanceFlags
        
        request = SanitationRequest(
            mode="general",
            place="home",
            profile=GuidanceFlags(pregnant=False, infant=False),
            issues=[]
        )
        
        items = _rule_based_checklist(request)
        
        assert len(items) >= 3  # Should have core sanitation steps
        assert any("hand hygiene" in item.title.lower() for item in items)
        assert any("disinfect" in item.title.lower() for item in items)

    def test_rule_based_checklist_flood_mode(self):
        """TC-BE-061: Test rule-based checklist for flood mode"""
        from api.guidance import _rule_based_checklist, SanitationRequest, GuidanceFlags
        
        request = SanitationRequest(
            mode="flood",
            place="home",
            profile=GuidanceFlags(pregnant=False, infant=False),
            issues=[]
        )
        
        items = _rule_based_checklist(request)
        
        assert len(items) >= 3  # Should have flood-specific steps
        assert any("bucket" in item.title.lower() for item in items)
        assert any("separate" in item.title.lower() for item in items)

    def test_rule_based_checklist_pregnancy_flag(self):
        """TC-BE-062: Test rule-based checklist with pregnancy flag"""
        from api.guidance import _rule_based_checklist, SanitationRequest, GuidanceFlags
        
        request = SanitationRequest(
            mode="general",
            place="home",
            profile=GuidanceFlags(pregnant=True, infant=False),
            issues=[]
        )
        
        items = _rule_based_checklist(request)
        
        # Should have pregnancy-specific items
        pregnancy_items = [item for item in items if "pregnancy" in item.title.lower() or "pads" in item.title.lower()]
        assert len(pregnancy_items) > 0

    def test_rule_based_checklist_infant_flag(self):
        """TC-BE-063: Test rule-based checklist with infant flag"""
        from api.guidance import _rule_based_checklist, SanitationRequest, GuidanceFlags
        
        request = SanitationRequest(
            mode="general",
            place="home",
            profile=GuidanceFlags(pregnant=False, infant=True),
            issues=[]
        )
        
        items = _rule_based_checklist(request)
        
        # Should have infant-specific items
        infant_items = [item for item in items if "infant" in item.title.lower() or "nappy" in item.title.lower()]
        assert len(infant_items) > 0

    @patch('api.guidance.OpenAI')
    def test_generate_llm_checklist_success(self, mock_openai, sample_sanitation_request, mock_openai_response):
        """TC-BE-064: Test successful LLM checklist generation"""
        from api.guidance import _generate_llm_checklist
        
        # Mock OpenAI client
        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = mock_openai_response
        
        result = _generate_llm_checklist(sample_sanitation_request)
        
        assert result is not None
        assert len(result.summary_top3) > 0
        assert len(result.sections) > 0

    @patch('api.guidance.OpenAI')
    def test_generate_llm_checklist_no_api_key(self, mock_openai, sample_sanitation_request):
        """TC-BE-065: Test LLM checklist generation without API key"""
        from api.guidance import _generate_llm_checklist
        
        with patch.dict('os.environ', {}, clear=True):
            result = _generate_llm_checklist(sample_sanitation_request)
            
            # Should return fallback response
            assert result is not None
            assert len(result.summary_top3) >= 0

    @patch('api.guidance.OpenAI')
    def test_generate_llm_checklist_api_error(self, mock_openai, sample_sanitation_request):
        """TC-BE-066: Test LLM checklist generation with API error"""
        from api.guidance import _generate_llm_checklist
        
        # Mock OpenAI client to raise exception
        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        result = _generate_llm_checklist(sample_sanitation_request)
        
        # Should return fallback response
        assert result is not None

    def test_fallback_checklist_response_pregnancy(self, sample_sanitation_request):
        """TC-BE-067: Test fallback checklist response with pregnancy flag"""
        from api.guidance import _fallback_checklist_response
        
        result = _fallback_checklist_response(sample_sanitation_request)
        
        assert result is not None
        assert len(result.summary_top3) > 0
        assert len(result.sections) > 0
        
        # Should have pregnancy-specific items
        pregnancy_items = [item for item in result.summary_top3 if "pads" in item.title.lower()]
        assert len(pregnancy_items) > 0

    def test_fallback_checklist_response_infant(self):
        """TC-BE-068: Test fallback checklist response with infant flag"""
        from api.guidance import _fallback_checklist_response, SanitationRequest, GuidanceFlags
        
        request = SanitationRequest(
            mode="general",
            place="home",
            profile=GuidanceFlags(pregnant=False, infant=True),
            issues=[]
        )
        
        result = _fallback_checklist_response(request)
        
        assert result is not None
        assert len(result.summary_top3) > 0
        
        # Should have infant-specific items
        infant_items = [item for item in result.summary_top3 if "infant" in item.title.lower()]
        assert len(infant_items) > 0

    def test_fallback_checklist_response_flood_mode(self):
        """TC-BE-069: Test fallback checklist response for flood mode"""
        from api.guidance import _fallback_checklist_response, SanitationRequest, GuidanceFlags
        
        request = SanitationRequest(
            mode="flood",
            place="home",
            profile=GuidanceFlags(pregnant=False, infant=False),
            issues=[]
        )
        
        result = _fallback_checklist_response(request)
        
        assert result is not None
        assert len(result.summary_top3) > 0
        
        # Should have flood-specific items
        flood_items = [item for item in result.summary_top3 if "bucket" in item.title.lower()]
        assert len(flood_items) > 0

    def test_checklist_api_endpoint_success(self, client, sample_sanitation_request):
        """TC-BE-070: Test checklist API endpoint success"""
        with patch('api.guidance._generate_llm_checklist') as mock_generate:
            from api.guidance import ChecklistResponse, ChecklistItem, ChecklistSection, ChecklistNote, ChecklistSource
            
            mock_item = ChecklistItem(title="Test Item")
            mock_section = ChecklistSection(name="Test Section", items=[mock_item])
            mock_note = ChecklistNote(type="general", text="Test note")
            mock_source = ChecklistSource(label="WHO", url="https://www.who.int")
            
            mock_response = ChecklistResponse(
                summary_top3=[mock_item],
                sections=[mock_section],
                notes=[mock_note],
                sources=[mock_source]
            )
            
            mock_generate.return_value = mock_response
            
            response = client.post("/api/guidance/checklist", json=sample_sanitation_request)
            
            assert response.status_code == 200
            data = response.json()
            assert "summary_top3" in data
            assert "sections" in data
            assert "notes" in data
            assert "sources" in data

    def test_checklist_api_endpoint_with_force(self, client, sample_sanitation_request):
        """TC-BE-071: Test checklist API endpoint with force parameter"""
        with patch('api.guidance._generate_llm_checklist') as mock_generate:
            from api.guidance import ChecklistResponse, ChecklistItem, ChecklistSection, ChecklistNote, ChecklistSource
            
            mock_item = ChecklistItem(title="Test Item")
            mock_section = ChecklistSection(name="Test Section", items=[mock_item])
            mock_note = ChecklistNote(type="general", text="Test note")
            mock_source = ChecklistSource(label="WHO", url="https://www.who.int")
            
            mock_response = ChecklistResponse(
                summary_top3=[mock_item],
                sections=[mock_section],
                notes=[mock_note],
                sources=[mock_source]
            )
            
            mock_generate.return_value = mock_response
            
            response = client.post("/api/guidance/checklist?force=true", json=sample_sanitation_request)
            
            assert response.status_code == 200
            mock_generate.assert_called_once()

    def test_explain_api_endpoint_success(self, client):
        """TC-BE-072: Test explain API endpoint success"""
        with patch('api.guidance.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client
            mock_client.chat.completions.create.return_value = Mock(
                choices=[Mock(message=Mock(content="This step is important for hygiene."))]
            )
            
            request_data = {
                "item_id": "hand-wash",
                "context": {"mode": "general", "place": "home"}
            }
            
            response = client.post("/api/guidance/explain", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "explanation" in data

    def test_explain_api_endpoint_no_api_key(self, client):
        """TC-BE-073: Test explain API endpoint without API key"""
        with patch.dict('os.environ', {}, clear=True):
            request_data = {
                "item_id": "hand-wash",
                "context": {"mode": "general", "place": "home"}
            }
            
            response = client.post("/api/guidance/explain", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "explanation" in data
            assert "hygiene and safety" in data["explanation"]

    def test_chat_api_endpoint_success(self, client):
        """TC-BE-074: Test chat API endpoint success"""
        with patch('api.guidance.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client
            mock_client.chat.completions.create.return_value = Mock(
                choices=[Mock(message=Mock(content="I can help with hygiene questions."))]
            )
            
            request_data = {
                "messages": [{"role": "user", "content": "How do I wash my hands?"}],
                "context": {"mode": "general", "place": "home"},
                "checklist": {},
                "sources": [{"label": "WHO", "url": "https://www.who.int"}]
            }
            
            response = client.post("/api/guidance/chat", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "sources" in data

    def test_chat_api_endpoint_no_api_key(self, client):
        """TC-BE-075: Test chat API endpoint without API key"""
        with patch.dict('os.environ', {}, clear=True):
            request_data = {
                "messages": [{"role": "user", "content": "How do I wash my hands?"}],
                "context": {"mode": "general", "place": "home"},
                "checklist": {},
                "sources": []
            }
            
            response = client.post("/api/guidance/chat", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "hygiene and sanitation" in data["message"]

    def test_legacy_sanitation_endpoint(self, client, sample_sanitation_request):
        """TC-BE-076: Test legacy sanitation endpoint for backward compatibility"""
        with patch('api.guidance._generate_llm_checklist') as mock_generate:
            from api.guidance import ChecklistResponse, ChecklistItem, ChecklistSection, ChecklistNote, ChecklistSource
            
            mock_item = ChecklistItem(title="Test Item")
            mock_section = ChecklistSection(name="Test Section", items=[mock_item])
            mock_note = ChecklistNote(type="general", text="Test note")
            mock_source = ChecklistSource(label="WHO", url="https://www.who.int")
            
            mock_response = ChecklistResponse(
                summary_top3=[mock_item],
                sections=[mock_section],
                notes=[mock_note],
                sources=[mock_source]
            )
            
            mock_generate.return_value = mock_response
            
            response = client.post("/api/guidance/sanitation", json=sample_sanitation_request)
            
            assert response.status_code == 200
            data = response.json()
            assert "checklist" in data
            assert len(data["checklist"]) > 0
