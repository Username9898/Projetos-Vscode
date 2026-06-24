# Multi-stage build para o frontend Next.js
FROM node:18-alpine AS builder

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY package.json package-lock.json* ./

# Instalar dependências
RUN npm ci --only=production && npm cache clean --force

# Copiar código fonte
COPY . .

# Build da aplicação
RUN npm run build

# ==================== STAGE FINAL ====================
FROM node:18-alpine AS runtime

# Metadados
LABEL maintainer="Roberto Ribeiro <contato@dentarium-ai.enterprise.com.br>"
LABEL description="Dentarium AI Enterprise - Frontend"
LABEL version="1.0.0"

# Criar usuário não-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Definir diretório de trabalho
WORKDIR /app

# Copiar dependências de produção
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules

# Copiar build da aplicação
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json

# Mudar para usuário não-root
USER nextjs

# Expor porta
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Comando de inicialização
CMD ["npm", "start"]