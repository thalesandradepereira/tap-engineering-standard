import {studioTemplates} from "./studioTemplates";
import {schema as createSchema} from "../endpoints/studio/create_POST.schema";
import {schema as saveSchema} from "../endpoints/studio/save_POST.schema";

describe("TAP Studio secure code templates",()=>{
  it("creates all three expected code assets",()=>{
    const data=studioTemplates.starter("Dashboard TAP");
    expect(data.html).toContain("Dashboard TAP");
    expect(data.css.length).toBeGreaterThan(50);
    expect(data.javascript).toContain("addEventListener");
  });
  it("keeps user names from introducing HTML tags",()=>{
    expect(studioTemplates.starter("<img src=x onerror=alert(1)>").html).not.toContain("<img");
  });
  it("accepts small files",()=>{
    expect(studioTemplates.assertDocument("<h1>A</h1>","body{}","console.log(1)")).toBe(true);
  });
  it("rejects files above 100KB",()=>{
    expect(()=>studioTemplates.assertDocument("A".repeat(100001),"","")).toThrow();
  });
  it("restricts UTF-8 bytes, not just JavaScript character count",()=>{
    expect(()=>studioTemplates.assertDocument("á".repeat(51000),"","")).toThrow();
  });
  it("escapes premature closing scripts and styles in standalone output",()=>{
    const html=studioTemplates.makePreview("<main>OK</main>","body{} </style>","console.log('</script>')");
    expect(html).toContain("<\\/style");
    expect(html).toContain("<\\/script");
  });
  it("isolates embedded preview network access when safe mode enabled",()=>{
    const html=studioTemplates.makePreview("<h1>OK</h1>","","",true);
    expect(html).toContain("Content-Security-Policy");
    expect(html).toContain("connect-src");
  });
  it("enforces reasonable project names",()=>{
    expect(createSchema.safeParse({name:"A"}).success).toBe(false);
    expect(createSchema.safeParse({name:"TAP Studio"}).success).toBe(true);
  });
  it("accepts only known project code files",()=>{
    const good={id:"123",files:{"index.html":"x","style.css":"","script.js":""}};
    expect(saveSchema.safeParse(good).success).toBe(true);
    expect(saveSchema.safeParse({...good,files:{...good.files,"secret.env":"TOKEN"}}).success).toBe(false);
  });
  it("rejects forged project IDs",()=>{
    expect(saveSchema.safeParse({id:"../x",files:{"index.html":"","style.css":"","script.js":""}}).success).toBe(false);
  });
});
