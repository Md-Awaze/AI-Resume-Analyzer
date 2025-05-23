// Test Scenarios
const testScenarios = {
    // Test Case 1: Perfect Resume
    perfectResume: {
        skills: ['JavaScript', 'Python', 'React', 'Node.js', 'SQL', 'AWS', 'Docker', 'Git'],
        suggestions: [
            'Your resume looks great! Consider adding more specific metrics for your achievements.',
            'You might want to highlight your soft skills more prominently.'
        ],
        matchScore: 95,
        status: 'Excellent match! Your resume is well-structured and comprehensive.'
    },

    // Test Case 2: Needs Improvement
    needsImprovement: {
        skills: ['JavaScript', 'HTML', 'CSS'],
        suggestions: [
            'Add more technical skills relevant to the position',
            'Include specific project achievements',
            'Add relevant certifications',
            'Expand on your work experience details'
        ],
        matchScore: 45,
        status: 'Your resume needs some improvements to better match the position.'
    },

    // Test Case 3: Error Case
    errorCase: {
        skills: [],
        suggestions: [],
        matchScore: 0,
        status: 'Error processing resume. Please try again.'
    }
};

// Test Functions
function runTests() {
    console.log('Starting Resume Analysis System Tests...');
    
    // Test 1: Perfect Resume
    console.log('\nTest 1: Perfect Resume');
    displayAnalysisResults(testScenarios.perfectResume);
    
    // Test 2: Needs Improvement (after 6 seconds)
    setTimeout(() => {
        console.log('\nTest 2: Needs Improvement');
        displayAnalysisResults(testScenarios.needsImprovement);
    }, 6000);
    
    // Test 3: Error Case (after 12 seconds)
    setTimeout(() => {
        console.log('\nTest 3: Error Case');
        displayAnalysisResults(testScenarios.errorCase);
    }, 12000);
}

// Run tests when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Add test controls to the page
    const testControls = document.createElement('div');
    testControls.className = 'test-controls';
    testControls.innerHTML = `
        <button onclick="runTests()">Run All Tests</button>
        <button onclick="displayAnalysisResults(testScenarios.perfectResume)">Test Perfect Resume</button>
        <button onclick="displayAnalysisResults(testScenarios.needsImprovement)">Test Needs Improvement</button>
        <button onclick="displayAnalysisResults(testScenarios.errorCase)">Test Error Case</button>
    `;
    document.body.insertBefore(testControls, document.body.firstChild);

    // Add some basic styles for the test controls
    const style = document.createElement('style');
    style.textContent = `
        .test-controls {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
        }
        .test-controls button {
            margin: 0 5px;
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            background: var(--primary-color);
            color: white;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .test-controls button:hover {
            background: #357abd;
        }
    `;
    document.head.appendChild(style);
}); 