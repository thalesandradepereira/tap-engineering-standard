import type { Selectable } from "kysely";
import type { StudioProjects } from "./schema";
export const studioProjectModel = {
  toClient(row:Selectable<StudioProjects>) {
    return {
      id:String(row.id),
      name:row.name,
      description:row.description,
      files:{
        "index.html":row.html,
        "style.css":row.css,
        "script.js":row.javascript
      },
      created_at: new Date(row.createdAt).toISOString(),
      updated_at: new Date(row.updatedAt).toISOString()
    };
  }
};
