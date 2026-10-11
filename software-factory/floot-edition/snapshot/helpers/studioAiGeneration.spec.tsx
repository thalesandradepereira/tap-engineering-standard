import {makeAiInstructions,parseGeneratedPage,validateGenerationRequest,extractGeneratedText} from "./studioAiGeneration";
describe("TAP AI Studio policy and output QA",()=>{
  it("rejects empty or extremely long prompts",()=>{
    expect(()=>validateGenerationRequest("")).toThrow();
    expect(()=>validateGenerationRequest("a".repeat(1501))).toThrow();
    expect(validateGenerationRequest("Página de indicadores TAP")).toBe("Página de indicadores TAP");
  });
  it("prevents provider prompt content from requesting credential access",()=>{
    const instructions=makeAiInstructions("TAP Teste 001");
    expect(instructions).toContain("JSON");
    expect(instructions).toContain("Do not request secrets");
  });
  it("parses the expected three-file JSON payload",()=>{
    const parsed=parseGeneratedPage(JSON.stringify({html:"<h1>Olá</h1>",css:"h1{color:red}",javascript:"console.log('ok')"}));
    expect(parsed["index.html"]).toBe("<h1>Olá</h1>");
    expect(parsed["style.css"]).toBe("h1{color:red}");
  });
  it("accepts fenced JSON but does not trust surrounding narrative",()=>{
    const parsed=parseGeneratedPage("NOISY\n\`\`\`json\n{\"html\":\"<main>OK</main>\",\"css\":\"\",\"javascript\":\"\"}\n\`\`\`");
    expect(parsed["index.html"]).toContain("<main>");
  });
  it("rejects oversized model output",()=>{
    expect(()=>parseGeneratedPage(JSON.stringify({html:"x".repeat(120001),css:"",javascript:""}))).toThrow();
  });
  it("rejects absent files and prototype-polluting extra keys",()=>{
    expect(()=>parseGeneratedPage('{"html":"<h1>OK</h1>","css":""}')).toThrow();
    expect(()=>parseGeneratedPage('{"html":"<h1>OK</h1>","css":"","javascript":"","__proto__":{"polluted":true}}')).toThrow();
  });
  it("rejects javascript URLs and dangerous externally-loaded scripts",()=>{
    expect(()=>parseGeneratedPage(JSON.stringify({html:'<script src="https://unknown.tld/a.js"></script><h1>ok</h1>',css:"",javascript:""}))).toThrow();
    expect(()=>parseGeneratedPage(JSON.stringify({html:'<a href="javascript:alert(1)">X</a>',css:"",javascript:""}))).toThrow();
  });
  it("rejects blank HTML",()=>{
    expect(()=>parseGeneratedPage(JSON.stringify({html:"   ",css:"a{}",javascript:""}))).toThrow();
  });

  it("parses a JSON object with commentary and braces inside strings",()=>{
    const sample=JSON.stringify({html:'<main data-label="{abc}">OK</main>',css:'main{color:blue}',javascript:'console.log("{x}")'});
    expect(parseGeneratedPage("Aqui está:\n"+sample+"\nFim.")["index.html"]).toContain("{abc}");
  });
  it("does not try to repair truncated JSON",()=>{
    expect(()=>parseGeneratedPage('{"html":"unfinished","css":"",')).toThrow();
  });
  it("detects an incomplete model response before JSON parsing",()=>{
    expect(()=>extractGeneratedText({status:"incomplete",incomplete_details:{reason:"max_output_tokens"},output_text:'{"html":"x"'})).toThrow();
  });
  it("supports both direct response text and fallback message content",()=>{
    expect(extractGeneratedText({status:"completed",output_text:'{"html":"OK"}'})).toContain('"html"');
    expect(extractGeneratedText({status:"completed",output:[{type:"message",content:[{type:"output_text",text:"fallback"}]}]})).toBe("fallback");
  });
});
