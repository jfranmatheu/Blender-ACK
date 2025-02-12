: Sync only the ackit folder from upstream:
call git fetch upstream
call git checkout main
call git read-tree --prefix=project-name/ackit upstream/main:ackit_addon_template/ackit
call git commit -m "Sync ackit folder from upstream"
