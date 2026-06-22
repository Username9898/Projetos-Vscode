import express from 'express';
import cors from 'cors';
import 'dotenv/config';
import { getGroqResponse } from './services/groqService.js';
import authRoutes from './routes/authRoutes.js';

const app = express();

app.use(cors());
app.use(express.json());

// Rotas de autenticação
app.use('/api/auth', authRoutes);

// Rota para testar a inteligência artificial Groq
app.post('/api/chat', async (req, res) => {
  const { prompt } = req.body;

  if (!prompt) {
    return res.status(400).json({ error: 'O campo "prompt" é obrigatório.' });
  }

  try {
    const aiResponse = await getGroqResponse(prompt);
    res.json({ reply: aiResponse });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Rota de saúde do servidor
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Servidor rodando na porta ${PORT}`);
});