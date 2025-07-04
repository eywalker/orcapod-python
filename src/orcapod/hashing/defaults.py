# A collection of utility function that provides a "default" implementation of hashers.
# This is often used as the fallback hasher in the library code.
from orcapod.hashing.types import CompositeFileHasher, ArrowHasher
from orcapod.hashing.file_hashers import PathLikeHasherFactory
from orcapod.hashing.string_cachers import InMemoryCacher
from orcapod.hashing.object_hashers import ObjectHasher
from orcapod.hashing.object_hashers import LegacyObjectHasher
from orcapod.hashing.function_info_extractors import FunctionInfoExtractorFactory
from orcapod.hashing.semantic_arrow_hasher import SemanticArrowHasher, PathHasher


def get_default_composite_file_hasher(with_cache=True) -> CompositeFileHasher:
    if with_cache:
        # use unlimited caching
        string_cacher = InMemoryCacher(max_size=None)
        return PathLikeHasherFactory.create_cached_composite(string_cacher)
    return PathLikeHasherFactory.create_basic_composite()


def get_default_composite_file_hasher_with_cacher(cacher=None) -> CompositeFileHasher:
    if cacher is None:
        cacher = InMemoryCacher(max_size=None)
    return PathLikeHasherFactory.create_cached_composite(cacher)


def get_default_object_hasher() -> ObjectHasher:
    function_info_extractor = (
        FunctionInfoExtractorFactory.create_function_info_extractor(
            strategy="signature"
        )
    )
    return LegacyObjectHasher(
        char_count=32, function_info_extractor=function_info_extractor
    )


def get_default_arrow_hasher(
    chunk_size: int = 8192, handle_missing: str = "error"
) -> ArrowHasher:
    hasher = SemanticArrowHasher(chunk_size=chunk_size, handle_missing=handle_missing)
    # register semantic hasher for Path
    hasher.register_semantic_hasher("Path", PathHasher())
    return hasher
