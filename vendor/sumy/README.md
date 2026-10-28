# Vendored Sumy packaging adjustment

Source: https://pypi.org/project/sumy/0.13.0/ (source archive SHA256 `5bdf1af5286801a74e9b5fd3aa58c3ab2316318a42de3c12f38f9737bee6cfc2`). The complete `sumy/` library source and data are unchanged; its upstream license is included.

Upstream 0.13.0 declares setuptools<82 as a runtime dependency, which retains known setuptools advisories. None of the library's Python modules imports setuptools or pkg_resources. The local pyproject.toml drops only that unused runtime dependency and requires a patched setuptools>=84.1 when building. This is a local packaging revision, not an upstream release or a new implementation of the summarization algorithms.

When refreshing this copy, compare the full upstream source and license, recheck runtime imports, resolve requirements, and scan the dependency graph. Remove this copy when an upstream release removes the constraint. The vendored upstream version must also be included in future advisory reviews.
