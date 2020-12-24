#include <Python.h>
#include <stdlib.h>
 
int Crand(int low, int high)
{
    return (rand() % (high - low)) + low;
}
 
static PyObject* crand(PyObject* self, PyObject* args)
{
    int low, high;
 
    if (!PyArg_ParseTuple(args, "ii", &low, &high))
        return NULL;
 
    return Py_BuildValue("i", Crand(low, high));
}

static PyObject* version(PyObject* self)
{
    return Py_BuildValue("s", "Version 1.0");
}
 
static PyMethodDef methods[] = {
    {"crand", crand, METH_VARARGS, "Return random number."},
    {"version", (PyCFunction)version, METH_NOARGS, "Returns the version."},
    {NULL, NULL, 0, NULL}
};
 
static struct PyModuleDef module = {
	PyModuleDef_HEAD_INIT,
	"crandom",
	"C-lib random module",
	-1,
	methods
};

PyMODINIT_FUNC PyInit_crandom(void)
{
    return PyModule_Create(&module);
}
