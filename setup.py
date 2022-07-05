from setuptools import setup

setup(
    name="signatureshape",
    version="0.2",
    packages=[
        "signatureshape",
        "signatureshape.se3",
        "signatureshape.se3.tests",
        "signatureshape.so3",
        "signatureshape.linear",
        "signatureshape.linear.experiments",
        "signatureshape.animation",
        "signatureshape.animation.db",
        "signatureshape.animation.src",
    ],
    url="",
    license="",
    author="Pål Erik Lystad ",
    author_email="",
    description="Fork of paalel/master so it can be install via pip",
    install_requries=[
        "pylab",
        "numpy",
        "iisignature",
        "matplotlib",
        "tvtk",
        "tqdm",
        "mayavi",
    ],
)
