import axios from 'axios';
export const getGroqResponse = async (prompt) => {
  try {
    const response = await axios.post('https://api.groq.com/openai/v1/chat/completions',{
      model:'llama-3.3-70b-versatile',
      messages:[{role:'user',content:prompt}],
      temperature:0.7
    },{
      headers:{'Authorization':`Bearer ${process.env.GROQ_API_KEY}`,'Content-Type':'application/json'}
    });
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('Erro na API do Groq:', error.response?.data || error.message);
    throw new Error('Falha ao processar requisição de IA.');
  }
};