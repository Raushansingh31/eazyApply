async function generateResume() {
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        linkedin: document.getElementById('linkedin').value,
        github: document.getElementById('github').value,
        style: document.getElementById('resumeStyle').value
    };

    try {
        const response = await fetch('/generate-resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        document.getElementById('previewContent').innerHTML = data.html;
    } catch (error) {
        console.error('Error generating resume:', error);
    }
}