---
name: tap-mobile-factory
description: Use quando o usuário solicitar aplicativo Android ou iOS, React Native, Expo, publicações em lojas, push notification, câmera, GPS ou sincronização offline.
---

# TAP Mobile Factory

## Execução
1. Triagem: PWA (sem loja), React Native/Expo, Flutter ou nativo. Preserve UX iOS/Android e distribuição exigida. PWA pode ser opção, mas não substitui APIs nativas indiscriminadamente.
2. Compartilhe contratos OpenAPI/types entre mobile e backend, nunca conecte diretamente a credenciais administrativas de banco.
3. Para Expo: gere código TypeScript, navegação, estados offline/online, permissões solicitadas minimamente, acesso seguro aos tokens (SecureStore em runtime apropriado), tratamento de erros e acessibilidade.
4. Inclua testes de componentes, navegação, login/logout, device rotation quando aplicável, internet interrompida, notificações, permissões negadas e sincronização sem duplicações.
5. Build iOS requer macOS/Xcode ou build remoto como EAS, certificados e Apple Developer; Android requer Android SDK/Gradle ou build remoto; publicação depende de contas de loja e revisão.
6. Não executar `npm`, `npx`, Expo/EAS nem comandos de instalação em máquina do usuário sem autorização e sem análise dos scripts do repositório.

## Entrega
Código e package lock quando instalações tiverem sido efetivamente autorizadas, config sem segredos, pipeline e instruções reproduzíveis. Distinguir preview, simulador, build assinado, instalação física, beta TestFlight/Play e app publicado na loja.

## Integração
O `tap-make-software` inclui este fluxo como sub-skill e indica provedor mobile disponível em cada execução. O plugin standalone não gera build na nuvem por conta própria.
