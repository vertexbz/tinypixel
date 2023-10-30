from sty import ef

FORMAT_SHORT = f"{ef.dim}[%(levelname)s]{ef.rs}[%(name)s] %(message)s"
FORMAT_DEBUG = f"{ef.dim}%(asctime)s [%(levelname)s]{ef.rs}[%(name)s] %(message)s {ef.dim}(%(relativepath)s:%(lineno)d){ef.rs}"
