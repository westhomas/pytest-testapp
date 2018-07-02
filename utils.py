import functools
from _pytest.assertion.rewrite import AssertionRewritingHook


def quiet(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        finalizers = []
        try:
            # When running pytest inline any plugins active in the main test
            # process are already imported.  So this disables the warning which
            # will trigger to say they can no longer be rewritten, which is
            # fine as they have already been rewritten.
            orig_warn = AssertionRewritingHook._warn_already_imported

            def revert_warn_already_imported():
                AssertionRewritingHook._warn_already_imported = orig_warn

            finalizers.append(revert_warn_already_imported)
            AssertionRewritingHook._warn_already_imported = lambda *a: None

            func(*args, **kwargs)
        finally:
            for finalizer in finalizers:
                finalizer()

    return wrapper