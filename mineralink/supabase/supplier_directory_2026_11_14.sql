-- MineraLink RDC · répertoire fournisseur à publication volontaire
-- Date : 2026-11-14 ; schéma appliqué au projet Supabase.
-- Pour une nouvelle instance uniquement : ne pas réexécuter sans vérifier les politiques existantes.
-- Les comptes non connectés n'ont aucun droit sur cette table.
create table public.supplier_directory (
 organization_id uuid primary key references public.organizations(id) on delete cascade,
 display_name text not null check (char_length(trim(display_name)) between 2 and 160),
 specialization text not null check (char_length(trim(specialization)) between 10 and 500),
 province text not null check (char_length(trim(province)) between 2 and 100),
 published_at timestamptz not null default now()
);
alter table public.supplier_directory enable row level security;
revoke all on public.supplier_directory from public, anon;
grant select, insert, update, delete on public.supplier_directory to authenticated;
create policy directory_read on public.supplier_directory for select to authenticated
 using (auth.uid() is not null);
create policy directory_publish on public.supplier_directory for insert to authenticated
 with check (auth.uid() is not null and public.is_org_owner(organization_id)
  and exists (select 1 from public.organizations o where o.id=organization_id and o.kind in ('supplier','both')));
create policy directory_edit on public.supplier_directory for update to authenticated
 using (public.is_org_owner(organization_id))
 with check (public.is_org_owner(organization_id)
  and exists (select 1 from public.organizations o where o.id=organization_id and o.kind in ('supplier','both')));
create policy directory_remove on public.supplier_directory for delete to authenticated
 using (public.is_org_owner(organization_id));
