function myFunction() {
    var age = document.getElementsByName('age')[0];
    var gender = document.getElementsByName('gender')[0];
    var exercise = document.getElementsByName('exercise')[0];
    var text = (age.options[age.selectedIndex].text) + (gender.options[gender.selectedIndex].text) + (exercise.options[exercise.selectedIndex].text);
    alert("The form was submitted " + text);
  }

const form = document.getElementById('genform');
const responseDiv = document.getElementById('response');

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const questionInput = document.getElementsByName('age')[0];
    const question = questionInput.value;
    
    if (question.trim() === '') {
        return;
    }
    
    responseDiv.innerHTML = 'Loading...';

    try {
        const response = await askChatGPT(question);
        responseDiv.innerHTML = response.data.choices[0].text.trim();
    } catch (error) {
        responseDiv.innerHTML = 'An error occurred.';
        console.error(error);
        alert(error);
    }
    
    questionInput.value = '';
});

async function askChatGPT(question) {
    const apiKey = '';
    const endpoint = 'https://api.openai.com/v1/chat/completions';
    
    const response = await axios.post(endpoint, {
        model: 'gpt-3.5-turbo',
        messages: [{ role: 'user', content: question }],
        temperature: 0,
        max_tokens: 7
    }, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        }
    });
    
    alert("it works");

    return response;
}
