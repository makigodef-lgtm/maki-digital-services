-- MineraLink secure backend foundation (Supabase PostgreSQL)
-- Apply in a private Supabase project after reviewing policies.
create extension if not exists pgcrypto;
create table public.organizations (
 id uuid primary key default gen_random_uuid(),
 name text not null check (char_length(name) between 2 and 160),
 kind text not null check (kind in ('buyer','supplier','both')),
 country_code text not null default 'CD' check (country_code ~ '^[A-Z]{2}$'),
 province text,
 verification_status text not null default 'unreviewed' check (verification_status in ('unreviewed','documents_received','under_review','verified','rejected')),
 created_at timestamptz not null default now()
);
create table public.memberships (
 organization_id uuid not null references public.organizations(id) on delete cascade,
 user_id uuid not null references auth.users(id) on delete cascade,
 role text not null check (role in ('owner','member')),
 primary key(organization_id,user_id)
);
create table public.rfqs (
 id uuid primary key default gen_random_uuid(),
 buyer_org_id uuid not null references public.organizations(id),
 title text not null check (char_length(title) between 5 and 180),
 description text not null check (char_length(description) between 20 and 5000),
 delivery_location text not null,
 currency text not null default 'USD' check (currency in ('USD','CDF')),
 status text not null default 'draft' check (status in ('draft','submitted','in_review','quoted','closed','cancelled')),
 created_by uuid not null default auth.uid() references auth.users(id),
 created_at timestamptz not null default now()
);
create table public.invitations (
 rfq_id uuid not null references public.rfqs(id) on delete cascade,
 supplier_org_id uuid not null references public.organizations(id),
 created_at timestamptz not null default now(),
 primary key(rfq_id,supplier_org_id)
);
create table public.quotes (
 id uuid primary key default gen_random_uuid(),
 rfq_id uuid not null,
 supplier_org_id uuid not null,
 amount numeric(18,2) not null check (amount >= 0),
 currency text not null check (currency in ('USD','CDF')),
 lead_days integer not null check (lead_days between 0 and 3650),
 notes text check (char_length(notes) <= 5000),
 status text not null default 'submitted' check (status in ('submitted','withdrawn')),
 created_by uuid not null default auth.uid() references auth.users(id),
 created_at timestamptz not null default now(),
 foreign key(rfq_id,supplier_org_id) references public.invitations(rfq_id,supplier_org_id)
);
create index on public.memberships(user_id);
create index on public.rfqs(buyer_org_id,status);
create index on public.invitations(supplier_org_id);
create index on public.quotes(rfq_id);
create function public.is_org_member(org uuid) returns boolean language sql stable security definer set search_path='' as $fn$
 select exists(select 1 from public.memberships m where m.organization_id=org and m.user_id=(select auth.uid()))
$fn$;
create function public.is_org_owner(org uuid) returns boolean language sql stable security definer set search_path='' as $fn$
 select exists(select 1 from public.memberships m where m.organization_id=org and m.user_id=(select auth.uid()) and m.role='owner')
$fn$;
revoke all on function public.is_org_member(uuid),public.is_org_owner(uuid) from public;
grant execute on function public.is_org_member(uuid),public.is_org_owner(uuid) to authenticated;
create function public.is_invited(request_id uuid) returns boolean language sql stable security definer set search_path='' as $fn$ select exists(select 1 from public.invitations i join public.memberships m on m.organization_id=i.supplier_org_id where i.rfq_id=request_id and m.user_id=(select auth.uid())) $fn$;
revoke all on function public.is_invited(uuid) from public;
grant execute on function public.is_invited(uuid) to authenticated;
alter table public.organizations enable row level security;
alter table public.memberships enable row level security;
alter table public.rfqs enable row level security;
alter table public.invitations enable row level security;
alter table public.quotes enable row level security;
create policy org_read on public.organizations for select to authenticated using (public.is_org_member(id));
create policy membership_read on public.memberships for select to authenticated using (public.is_org_member(organization_id));
create policy rfq_read on public.rfqs for select to authenticated using (public.is_org_member(buyer_org_id) or public.is_invited(id));
create policy rfq_create on public.rfqs for insert to authenticated with check (public.is_org_member(buyer_org_id) and created_by=(select auth.uid()) and status='draft');
create policy invitation_read on public.invitations for select to authenticated using (public.is_org_member(supplier_org_id));
create policy quote_read on public.quotes for select to authenticated using (public.is_org_member(supplier_org_id) or exists(select 1 from public.rfqs r where r.id=rfq_id and public.is_org_member(r.buyer_org_id)));
create policy quote_create on public.quotes for insert to authenticated with check (public.is_org_member(supplier_org_id) and created_by=(select auth.uid()) and status='submitted' and exists(select 1 from public.rfqs r where r.id=rfq_id and r.status in ('submitted','in_review','quoted')));
-- All mutations not explicitly permitted above are denied. Organization creation,
-- owner enrollment, verification, invitations, RFQ submission and status changes
-- MUST use audited server-side functions with role checks, not client-side service keys.

revoke all on table public.organizations,public.memberships,public.rfqs,public.invitations,public.quotes from anon,authenticated;
grant select on table public.organizations,public.memberships,public.rfqs,public.invitations,public.quotes to authenticated;
grant insert on table public.rfqs,public.quotes to authenticated;
