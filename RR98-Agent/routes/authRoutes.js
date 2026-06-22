import { Router } from 'express';
import jwt from 'jsonwebtoken';

const router = Router();
const JWT_SECRET = process.env.JWT_SECRET || 'rr98-agent-secret-key';

// Login simplificado
router.post('/login', (req, res) => {
  const { username, password } = req.body;
  
  // Credenciais padrão - em produção usar banco de dados
  if (username === 'admin' && password === 'rr98@2026') {
    const token = jwt.sign({ username, role: 'admin' }, JWT_SECRET, { expiresIn: '24h' });
    return res.json({ token, user: { username, role: 'admin' } });
  }

  res.status(401).json({ error: 'Credenciais inválidas' });
});

// Verificar token
router.get('/verify', (req, res) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) return res.status(401).json({ error: 'Token não fornecido' });

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    res.json({ valid: true, user: decoded });
  } catch {
    res.status(401).json({ error: 'Token inválido' });
  }
});

export default router;