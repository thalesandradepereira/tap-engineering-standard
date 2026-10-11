# Recipes — arquiteturas por necessidade

## 1. Landing page / dashboard / PWA leve
Vite + TypeScript ou HTML/CSS/JS com layout responsivo, acessibilidade, testes de componentes e GitHub Pages/Cloudflare Pages. `localStorage` somente para preferências/dados locais não sensíveis. Para múltiplos usuários introduzir backend real. Serviço worker não existe no GitHub Pages.

## 2. SaaS com login e banco
React/Next.js conforme requisitos de SEO e servidor; API FastAPI ou Node; PostgreSQL (ou MongoDB com escolha explícita), autenticação gerenciada, RBAC no servidor e migrações. Diagrama: `Usuário → UI HTTPS → API/Auth → Banco/filestore`, com logs/backup separados. Tenancy explícito, política de retenção, MFA para administradores, auditoria de ações, billing sandbox. Evite adotar integrações por popularidade sem inspecionar termos e custos.

## 3. Mobile iOS/Android
Expo + React Native/TypeScript, API compartilhada, armazenamento seguro de tokens, permissões mínimas, telas offline e sincronização; testar em Expo Go quando compatível e device real antes das lojas. APK/AAB/IPA exigem build service/contas; não declarar gerado se não houve build.

## 4. Agentes com IA e integrações
Ferramentas com schemas exatos, auth, escopo, timeout, retry controlado, idempotência, logs redigidos. RAG: permissão de documentos, proveniência, citações por fonte, defesas contra injeção, avaliação de fidelidade e custo por consulta. MCP apenas quando existe servidor real.

## 5. Dashboard analítico
Definir granularidade, chaves, fontes oficiais, normalização e agregações antes da UI. Testar totais contra origem, cross-filter bidirecional, filtros combinados, drill-down, exportação consistente e grandes volumes.

## 6. Formulário de avaliação física em academia
Modelo com consentimento, perfil, histórico de atividade, anotações e mapa corporal acessível com regiões selecionáveis, intensidade e lateralidade; visuais anatômicos são auxiliares. Não inferir diagnósticos nem personalizar exercícios clínicos a partir de um mapa isolado; pedir revisão por profissional habilitado quando houver dor ou condição de saúde. Caso multiusuário, dados protegidos, autenticação e banco apropriado; GitHub Pages sozinho é insuficiente.

## Decisões obrigatórias antes de release
Status de autenticação real vs simulada; onde dados persistem; quem paga hospedagem/serviços; quem controla DNS, lojas e keys; como restaura backup; como desfaz deploy; evidência do teste final.
