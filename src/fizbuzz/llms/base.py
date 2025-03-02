import abc
import typing as t


class LLMBase(abc.ABCMeta):
    def __init__(self):
        raise AttributeError("Cannot instansiate a namespace class")

    @classmethod
    @abc.abstractmethod
    def get_llm(cls, **llm_params: dict[str, t.Any]) -> t.Any:
        raise NotImplementedError(
            "`get_llm` method not implememnted, implememnt it first"
        )

    @classmethod
    @abc.abstractmethod
    def get_default_llm(
        cls, model_name: str, temprature: str, **llm_param: str
    ) -> t.Any:
        raise NotImplementedError("`get_default_llm` method not implemented.")
