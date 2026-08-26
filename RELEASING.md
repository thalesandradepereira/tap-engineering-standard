# Release Integrity / Integridade de Releases

## English

TAP Engineering Standard intentionally keeps its validation path dependency-free. Release integrity should therefore rely on Git provenance, deterministic artifacts, and SHA-256 verification rather than introducing a package manager or an opaque publishing action.

### Maintainer release procedure

1. Start from a clean, reviewed `main` commit with the validation workflow green.
2. Create a signed annotated tag with a configured GPG or SSH signing identity. Do not create or share private signing keys through repository automation.
3. Verify the tag locally before publishing it.
4. Build the deterministic skill bundle:

```bash
python3 scripts/build_release_bundle.py
```

This creates:

```text
dist/tap-engineering-standard-skill.zip
dist/SHA256SUMS
```

5. Publish both files together as release assets for the exact signed tag.
6. Record the tagged commit SHA in the release notes.

Example signed-tag flow when Git signing is already configured:

```bash
git switch main
git pull --ff-only
git tag -s vX.Y.Z -m "TAP Engineering Standard vX.Y.Z"
git tag -v vX.Y.Z
git push origin vX.Y.Z
```

### Consumer verification

Automated installations should pin an exact tag or commit rather than a floating branch. When using a published release bundle, download both assets and verify the archive before importing the Skill:

```bash
sha256sum -c SHA256SUMS
```

On systems without `sha256sum`, compute SHA-256 with a trusted local tool and compare it with the value in `SHA256SUMS`.

A checksum proves that the downloaded archive matches the published checksum. A verified signed tag additionally provides maintainer provenance. Neither should be described as verified unless the corresponding check was actually performed.

## Português do Brasil

O TAP Engineering Standard mantém deliberadamente o caminho de validação sem dependências externas. Por isso, a integridade de releases deve se apoiar em proveniência Git, artefatos determinísticos e verificação SHA-256, em vez de introduzir gerenciadores de pacotes ou actions de publicação opacas.

### Procedimento de release para o mantenedor

1. Parta de um commit limpo e revisado do `main`, com o workflow de validação aprovado.
2. Crie uma tag anotada e assinada usando uma identidade GPG ou SSH já configurada. Não crie nem compartilhe chaves privadas de assinatura por automações do repositório.
3. Verifique a tag localmente antes da publicação.
4. Gere o bundle determinístico da Skill:

```bash
python3 scripts/build_release_bundle.py
```

Serão criados:

```text
dist/tap-engineering-standard-skill.zip
dist/SHA256SUMS
```

5. Publique os dois arquivos juntos como assets da release correspondente à tag assinada.
6. Registre o SHA exato do commit da tag nas notas da release.

Exemplo quando a assinatura Git já estiver configurada:

```bash
git switch main
git pull --ff-only
git tag -s vX.Y.Z -m "TAP Engineering Standard vX.Y.Z"
git tag -v vX.Y.Z
git push origin vX.Y.Z
```

### Verificação pelo consumidor

Instalações automatizadas devem fixar uma tag ou commit exato, evitando branches flutuantes. Ao usar um bundle de release publicado, baixe os dois assets e valide o arquivo antes de importar a Skill:

```bash
sha256sum -c SHA256SUMS
```

Em sistemas sem `sha256sum`, calcule o SHA-256 com uma ferramenta local confiável e compare com o valor de `SHA256SUMS`.

O checksum comprova que o arquivo baixado corresponde ao checksum publicado. Uma tag assinada e verificada adiciona evidência de proveniência do mantenedor. Nenhuma dessas verificações deve ser declarada como concluída sem que o respectivo teste tenha sido realmente executado.
