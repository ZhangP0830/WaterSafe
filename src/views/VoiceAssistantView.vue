<script setup>
import { onMounted, onUnmounted } from "vue";

// import components
import NavbarDefault from "../components/navigation/NavbarDefault.vue";
import DefaultFooter from "../components/layout/FooterDefault.vue";
import MaterialButton from "@/components/MaterialButton.vue";

// page lifecycle
const body = document.getElementsByTagName("body")[0];
onMounted(() => {
  body.classList.add("voice-assistant-page");
  body.classList.add("bg-gray-100");
  
  // dynamically load ElevenLabs script
  loadElevenLabsScript();
});

onUnmounted(() => {
  body.classList.remove("voice-assistant-page");
  body.classList.remove("bg-gray-100");
});

// function to load ElevenLabs script
const loadElevenLabsScript = () => {
  // check if the script is already loaded
  if (document.querySelector('script[src*="convai-widget-embed"]')) {
    return;
  }
  
  const script = document.createElement('script');
  script.src = 'https://unpkg.com/@elevenlabs/convai-widget-embed';
  script.async = true;
  script.type = 'text/javascript';
  document.head.appendChild(script);
};

// scroll to features section
const scrollToFeatures = () => {
  const featuresElement = document.getElementById('features');
  if (featuresElement) {
    featuresElement.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
  }
};

// features data
const features = [
  {
    icon: "mic",
    title: "Voice Interaction",
    description: "Speak naturally with our AI companion using advanced voice recognition technology."
  },
  {
    icon: "psychology",
    title: "Smart Responses",
    description: "Get intelligent, contextual responses about water safety and quality information."
  },
  {
    icon: "accessibility",
    title: "Accessible Design",
    description: "Voice-first interface makes water safety information accessible to everyone."
  },
  {
    icon: "support_agent",
    title: "24/7 Support",
    description: "Get instant help and guidance about water safety concerns anytime, anywhere."
  }
];

// usage steps
const usageSteps = [
  {
    step: "1",
    title: "Click the Water Safety Companion",
    description: "Click on the companion widget that appears on the page to start a conversation."
  },
  {
    step: "2", 
    title: "Allow Microphone Access",
    description: "Grant microphone permissions when prompted to enable voice interaction."
  },
  {
    step: "3",
    title: "Start Speaking",
    description: "Ask questions about water safety, contamination, or any water-related concerns."
  },
  {
    step: "4",
    title: "Get Instant Answers",
    description: "Receive immediate, accurate responses from our AI-powered water safety expert."
  }
];
</script>

<template>
  <!-- navbar -->
  <div class="container position-sticky z-index-sticky top-0 navbar-container">
    <div class="row">
      <div class="col-12">
        <NavbarDefault :sticky="true" />
      </div>
    </div>
  </div>

  <!-- main content section -->
  <div class="container-fluid px-4 mt-6 pt-5 main-content">
    <!-- Page Introduction -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <h4 class="mb-3 text-center">
              <i class="material-icons me-2 text-info">mic</i>
              Water Safety Companion
            </h4>
            <p class="text-muted mb-3 text-center">
              This AI assistant provides instant water safety guidance through voice conversation. Click the microphone button to start speaking, or type your questions in the chat box. Ask about water quality, contamination signs, safety measures, or emergency procedures. The assistant will provide expert advice and step-by-step guidance for your specific situation.
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- features section -->
    <section class="py-5" id="features">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 text-center mx-auto mb-5">
            <h2 class="text-gradient text-primary mb-3">Water Safety Companion Features</h2>
            <p class="lead">
              Our AI-powered companion provides comprehensive water safety information 
              through natural conversation. Experience the future of water safety guidance.
            </p>
          </div>
        </div>
        
        <div class="row">
          <div 
            v-for="feature in features" 
            :key="feature.title"
            class="col-lg-3 col-md-6 mb-4"
          >
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="icon icon-shape icon-lg bg-gradient-primary shadow mx-auto mb-3">
                  <i class="material-icons text-white">{{ feature.icon }}</i>
                </div>
                <h5 class="fw-bold">{{ feature.title }}</h5>
                <p class="text-muted">{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- usage steps section -->
    <section class="py-5 bg-gray-100">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 text-center mx-auto mb-5">
            <h2 class="text-gradient text-primary mb-3">How to Use</h2>
            <p class="lead">
              Getting started with our Water Safety Companion is simple. Follow these easy steps 
              to begin your water safety conversation.
            </p>
          </div>
        </div>
        
        <div class="row">
          <div 
            v-for="step in usageSteps" 
            :key="step.step"
            class="col-lg-6 col-md-6 mb-4"
          >
            <div class="card border-0 shadow-sm h-100">
              <div class="card-body p-4">
                <div class="d-flex align-items-start">
                  <div class="icon icon-shape icon-sm bg-gradient-primary text-white rounded-circle me-3">
                    <span class="fw-bold">{{ step.step }}</span>
                  </div>
                  <div>
                    <h6 class="fw-bold mb-2">{{ step.title }}</h6>
                    <p class="text-muted mb-0">{{ step.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- voice assistant activation section -->
    <section class="py-5">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 text-center mx-auto">
            <h2 class="text-gradient text-primary mb-3">Start Your Conversation</h2>
            <p class="lead mb-4">
              The Water Safety Companion widget is now active on this page. Look for the conversation 
              widget and click to start talking about water safety.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>

  <!-- ElevenLabs conversation component -->
  <elevenlabs-convai agent-id="agent_5201k4856sm6fa1sna9v4hr7xev5"></elevenlabs-convai>

  <!-- footer -->
  <DefaultFooter />
</template>

<style scoped>
/* Ensure proper spacing between navigation and content */
.navbar-container {
  margin-bottom: 3rem;
}

.main-content {
  margin-top: 4rem;
  padding-top: 2rem;
}

.bg-gray-100 {
  background-color: #f8f9fa !important;
}

.bg-gray-200 {
  background-color: #e9ecef !important;
}

.icon-shape {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.icon-shape i {
  position: static !important;
  top: auto !important;
  transform: none !important;
}

.ni {
  font-family: 'Nucleo Icons';
}

/* voice assistant style */
elevenlabs-convai {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

/* responsive adjustment */
@media (max-width: 768px) {
  .display-3 {
    font-size: 2.5rem;
  }
  
  .lead {
    font-size: 1.1rem !important;
  }
  
  elevenlabs-convai {
    bottom: 10px;
    right: 10px;
  }
}

/* animation effect */
.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
}

.icon-shape {
  transition: transform 0.2s ease-in-out;
}

.icon-shape:hover {
  transform: scale(1.1);
}

/* gradient text */
.text-gradient {
  background: linear-gradient(45deg, #007bff, #0056b3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
