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

-- Floot AI Builder v0.2.0; requires existing Floot-managed users and studio_projects tables.
CREATE TABLE IF NOT EXISTS studio_ai_entitlements(
 user_id integer PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
 enabled boolean NOT NULL DEFAULT false,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS studio_ai_requests(
 id bigserial PRIMARY KEY,
 user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 project_id bigint NOT NULL REFERENCES studio_projects(id) ON DELETE CASCADE,
 requested_at timestamptz NOT NULL DEFAULT now(),
 status varchar(24) NOT NULL CHECK(status IN ('started','completed','failed')),
 credits_consumed numeric(16,4) NOT NULL DEFAULT 0 CHECK(credits_consumed>=0)
);
CREATE INDEX IF NOT EXISTS studio_ai_requests_user_date_idx ON studio_ai_requests(user_id, requested_at DESC);
-- Individual access grants require an authorized operator; no account IDs or secrets published.
