export const studioTemplates = {
  allowedFiles: ["index.html","style.css","script.js"] as const,
  starter(name: string) {
    const title = name.replace(/[<>&"']/g, "").slice(0,80);
    return {
      html: '<main class="container"><p class="eyebrow">TAP Creative Lab</p><h1>Bem-vindo ao ' + title + '</h1><p>Edite HTML, CSS e JavaScript para começar seu aplicativo.</p><button id="go">Começar</button></main>',
      css: 'body{background:#f7f6f1;color:#152927;font-family:system-ui;margin:0}.container{max-width:620px;margin:19vh auto;text-align:center}.eyebrow{color:#27967f;text-transform:uppercase;letter-spacing:.18em}h1{font-size:clamp(32px,7vw,52px)}button{padding:13px 26px;background:#152927;color:white;border:0;border-radius:8px;cursor:pointer}',
      javascript: 'document.getElementById("go")?.addEventListener("click",()=>alert("Made by TAP"));'
    };
  },
  assertDocument(html:string, css:string, javascript:string) {
    const items = [html,css,javascript];
    if(items.some(v => typeof v !== "string" || new TextEncoder().encode(v).length>100000)){
      throw new Error("Limite de 100 KB por arquivo.");
    }
    return true;
  },
  makePreview(html:string,css:string,javascript:string,restricted=false) {
    const safeCss=css.replace(/<\/style/gi,"<\\/style");
    const safeJs=javascript.replace(/<\/script/gi,"<\\/script");
    const meta = restricted ? '<meta http-equiv="Content-Security-Policy" content="default-src &#39;none&#39;; base-uri &#39;none&#39;; connect-src &#39;none&#39;; form-action &#39;none&#39;; frame-src &#39;none&#39;; img-src data:; style-src &#39;unsafe-inline&#39;; script-src &#39;unsafe-inline&#39;">' : '';
    return '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+meta+'<style>'+safeCss+'</style></head><body>'+html+'<script>'+safeJs+'</'+'script></body></html>';
  }
};
