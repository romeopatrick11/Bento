import os

#from pyext \
#    import \
#        pycc_task
from task_manager \
    import \
        extension, get_extension_hook
from task \
    import \
        Task
from compiled_fun \
    import \
        compile_fun
from utils \
    import \
        ensure_dir

swig_func, swig_vars = compile_fun("swig", "${SWIG} ${SWIGFLAGS} -o ${TGT[0]} ${SRC}", False)

@extension(".i")
def swig_hook(self, name):
    # FIXME: only handle C extension (no C++)
    base = os.path.splitext(name)[0]
    target = os.path.join(self.env["BLDDIR"], base)
    targets = [target + "_wrap.c", target + ".py"]
    for t in targets:
        ensure_dir(t)
    task = Task("swig", inputs=name, outputs=targets)
    task.func = swig_func
    task.env_vars = swig_vars
    task.env = self.env

    compile_task = get_extension_hook(".c")
    ctask = compile_task(self, targets[0])
    return [task] + ctask
