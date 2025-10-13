#!/usr/bin/env node

/**
 * WaterSafe Test Execution Script
 * 
 * This script provides a comprehensive test execution framework
 * with detailed reporting and quality metrics.
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class TestRunner {
  constructor() {
    this.testResults = {
      total: 0,
      passed: 0,
      failed: 0,
      skipped: 0,
      coverage: 0,
      startTime: null,
      endTime: null,
      duration: 0
    };
    
    this.testSuites = [
      'HomeView.test.js',
      'MaternalInfantHealth.test.js', 
      'Navigation.test.js',
      'WaterHealthInfo.test.js'
    ];
  }

  async runTests() {
    console.log('🧪 WaterSafe Test Suite Execution');
    console.log('=====================================\n');
    
    this.testResults.startTime = new Date();
    
    try {
      // Check if test dependencies are installed
      this.checkDependencies();
      
      // Run the test suite
      console.log('📋 Running comprehensive test suite...\n');
      
      const testCommand = 'npm run test:run';
      const output = execSync(testCommand, { 
        encoding: 'utf8',
        stdio: 'pipe'
      });
      
      this.parseTestResults(output);
      this.generateReport();
      
    } catch (error) {
      console.error('❌ Test execution failed:', error.message);
      this.testResults.failed++;
      this.generateErrorReport(error);
    }
    
    this.testResults.endTime = new Date();
    this.testResults.duration = this.testResults.endTime - this.testResults.startTime;
    
    return this.testResults;
  }

  checkDependencies() {
    console.log('🔍 Checking test dependencies...');
    
    const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    const requiredDeps = [
      '@vue/test-utils',
      'vitest',
      'jsdom',
      '@testing-library/vue'
    ];
    
    const missingDeps = requiredDeps.filter(dep => 
      !packageJson.devDependencies[dep]
    );
    
    if (missingDeps.length > 0) {
      throw new Error(`Missing dependencies: ${missingDeps.join(', ')}`);
    }
    
    console.log('✅ All dependencies are installed\n');
  }

  parseTestResults(output) {
    console.log('📊 Parsing test results...\n');
    
    // Extract test statistics from vitest output
    const lines = output.split('\n');
    
    for (const line of lines) {
      if (line.includes('Tests:')) {
        const match = line.match(/(\d+) passed|(\d+) failed|(\d+) skipped/g);
        if (match) {
          match.forEach(m => {
            if (m.includes('passed')) {
              this.testResults.passed = parseInt(m.match(/\d+/)[0]);
            } else if (m.includes('failed')) {
              this.testResults.failed = parseInt(m.match(/\d+/)[0]);
            } else if (m.includes('skipped')) {
              this.testResults.skipped = parseInt(m.match(/\d+/)[0]);
            }
          });
        }
      }
      
      if (line.includes('Coverage:')) {
        const coverageMatch = line.match(/(\d+\.?\d*)%/);
        if (coverageMatch) {
          this.testResults.coverage = parseFloat(coverageMatch[1]);
        }
      }
    }
    
    this.testResults.total = this.testResults.passed + this.testResults.failed + this.testResults.skipped;
  }

  generateReport() {
    console.log('📈 Test Execution Report');
    console.log('========================\n');
    
    console.log(`⏱️  Duration: ${this.testResults.duration}ms`);
    console.log(`📊 Total Tests: ${this.testResults.total}`);
    console.log(`✅ Passed: ${this.testResults.passed}`);
    console.log(`❌ Failed: ${this.testResults.failed}`);
    console.log(`⏭️  Skipped: ${this.testResults.skipped}`);
    console.log(`📈 Coverage: ${this.testResults.coverage}%\n`);
    
    // Quality Assessment
    this.assessQuality();
    
    // Recommendations
    this.generateRecommendations();
    
    // Save detailed report
    this.saveDetailedReport();
  }

  assessQuality() {
    console.log('🎯 Quality Assessment');
    console.log('====================\n');
    
    const passRate = (this.testResults.passed / this.testResults.total) * 100;
    
    if (passRate === 100) {
      console.log('🟢 EXCELLENT: All tests passed!');
    } else if (passRate >= 90) {
      console.log('🟡 GOOD: Most tests passed, minor issues to address');
    } else if (passRate >= 80) {
      console.log('🟠 FAIR: Some tests failed, review and fix issues');
    } else {
      console.log('🔴 POOR: Many tests failed, significant issues to address');
    }
    
    if (this.testResults.coverage >= 80) {
      console.log('🟢 Coverage: Excellent test coverage');
    } else if (this.testResults.coverage >= 60) {
      console.log('🟡 Coverage: Good test coverage, room for improvement');
    } else {
      console.log('🔴 Coverage: Low test coverage, needs improvement');
    }
    
    console.log('');
  }

  generateRecommendations() {
    console.log('💡 Recommendations');
    console.log('==================\n');
    
    if (this.testResults.failed > 0) {
      console.log('🔧 Fix failing tests before deployment');
      console.log('📝 Review test cases for accuracy and completeness');
    }
    
    if (this.testResults.coverage < 80) {
      console.log('📈 Increase test coverage to meet quality standards');
      console.log('🎯 Focus on critical user paths and edge cases');
    }
    
    if (this.testResults.skipped > 0) {
      console.log('⏭️  Review skipped tests and implement if needed');
    }
    
    console.log('🔄 Run tests regularly during development');
    console.log('📊 Monitor test metrics and quality trends\n');
  }

  saveDetailedReport() {
    const report = {
      timestamp: new Date().toISOString(),
      summary: this.testResults,
      testSuites: this.testSuites,
      quality: {
        passRate: (this.testResults.passed / this.testResults.total) * 100,
        coverage: this.testResults.coverage,
        status: this.testResults.failed === 0 ? 'PASS' : 'FAIL'
      }
    };
    
    const reportPath = path.join(__dirname, 'test-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    
    console.log(`📄 Detailed report saved to: ${reportPath}`);
  }

  generateErrorReport(error) {
    console.log('❌ Error Report');
    console.log('===============\n');
    console.log(`Error: ${error.message}`);
    console.log('Stack:', error.stack);
    console.log('\n🔧 Troubleshooting:');
    console.log('1. Ensure all dependencies are installed: npm install');
    console.log('2. Check Node.js version compatibility');
    console.log('3. Verify test file syntax and imports');
    console.log('4. Run individual test files to isolate issues\n');
  }
}

// Execute tests if run directly
if (require.main === module) {
  const runner = new TestRunner();
  runner.runTests().then(results => {
    process.exit(results.failed > 0 ? 1 : 0);
  }).catch(error => {
    console.error('Test execution failed:', error);
    process.exit(1);
  });
}

module.exports = TestRunner;
