-- TAP Studio Floot Edition v0.1 — reference migration, already provisioned on Floot
-- Apply only to a DB with its Floot-managed users(id) table.
CREATE TABLE IF NOT EXISTS studio_projects (
 id bigserial PRIMARY KEY,
 owner_user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 name varchar(80) NOT NULL CHECK(length(trim(name)) >= 2),
 description varchar(240) NOT NULL DEFAULT '',
 html text NOT NULL DEFAULT '', css text NOT NULL DEFAULT '', javascript text NOT NULL DEFAULT '',
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now(),
 CONSTRAINT html_limit CHECK(octet_length(html) <= 100000),
 CONSTRAINT css_limit CHECK(octet_length(css) <= 100000),
 CONSTRAINT javascript_limit CHECK(octet_length(javascript) <= 100000)
);
CREATE INDEX IF NOT EXISTS studio_projects_owner_updated_idx ON studio_projects(owner_user_id,updated_at DESC);
