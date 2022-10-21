"""Tests the integration of the different modules used in your wrapper.

This file is meant to contain tests that verify that the different components
of your software are also functional when they have to work together.

Modify this file to adapt it to your own wrapper. You can organize your tests
in any way you wish (e.g. distribute them among different files) and use any
testing framework, and you can omit this kind of testing in your package,
although it is recommended not to do so.
"""

import unittest
from functools import wraps
from inspect import getfullargspec
from typing import get_type_hints

from package_name.wrapper import SimulationWrapper


class TestIntegrationWrapperEngine(unittest.TestCase):
    """Tests the integration of the wrapper and the engine classes.

    As the engine is simple, only a test that checks that the correct types are
    passed by the wrapper to the engine functions is provided. As the
    consistency check of the wrapper already checks that the dimension or data
    types of the arrays passed by the wrapper are correct, this coverage should
    be sufficient.

    Nevertheless, always be on guard:
        "A software tester walks into a bar. Asks to be seated outside, behind
        the counter and in the basement. Orders 1 beer, 374738493 beers, -3
        beers, 'asdfgh' beers, a mojito, 5.8 mojitos and a Rubik's Cube. Jumps
        on and dances on all the tables. Testing is complete.

        The bar opens to the public and after a few hour a customer comes in
        and asks where the bathroom is. The bar explodes and bursts into
        flames."
    """

    def test_types_engine(self):
        """Test that correct types are passed to the engine functions.

        Tests that the correct types are passed to the engine functions. The
        engine functions are only called when the `commit` and `compute`
        functions from the wrapper API are called. And actually `compute` calls
        commit. Therefore, this test just needs to run a simulation to verify
        all calls made to the engine.

        Actually this is something that you would do, at least for the static
        case, with a type checker such as mypy. However, it is a pretty good
        example of an integration test, that is why it is included.
        """
        from simphony_osp.namespaces import ontology_namespace as namespace
        from simphony_osp.wrappers import SimulationWrapper

        # decorate the methods on the engine so that they verify the declared
        # type hints
        session = SimulationWrapper()
        wrapper = session.driver.interface
        # read the diagram on the SimPhoNy documentation to understand how the
        # wrapper object was retrieved from the session object:
        # https://simphony.readthedocs.io/en/v4.0.0rc4/developers/
        # wrappers.html#wrapper-abstract-class
        session.driver.interface = self._prepare_wrapper_for_types_test(
            wrapper
        )

        # run a simulation, that should raise no validation errors

        with session:
            atm = namespace.Atom()
            pos = namespace.Position(value=[8, 5, 3], unit="m")
            vel = namespace.Velocity(value=[1, 2, 3], unit="m/s")
            atm[namespace.hasPart] = pos, vel
            session.compute(time_steps=5)

    @staticmethod
    def _prepare_wrapper_for_types_test(
        wrapper: SimulationWrapper,
    ) -> SimulationWrapper:
        """Decorate relevant engine functions with a type-checking decorator.

        The type-checking decorator verifies that the types that are passed
        to the engine functions match the type hints defined in their
        signature.

        Actually this is something that you would do, at least for the static
        case, with a type checker such as mypy. However, it is a pretty good
        example of an integration test, that is why it is included.
        """
        # prepare a decorator to validate type hints
        class ValidationError(Exception):
            """Specific exception to be used only in this test."""

            pass

        def verify_hints(method):
            """Makes the decorated function validate type hints.

            The method to decorate must be a bound method.
            """

            @wraps(method)
            def decorated(*args, **kwargs):
                hints_kwargs = {argument: None for argument in kwargs}
                hints_args = {
                    argument: None
                    for argument in getfullargspec(method).args[
                        1:
                    ]  # exclude "self"
                    if argument not in hints_kwargs
                }
                hints_return = None
                for argument, type_ in get_type_hints(method).items():
                    if argument == "return":
                        hints_return = type_
                    elif argument in hints_kwargs:
                        hints_kwargs[argument] = type_
                    else:
                        hints_args[argument] = type_

                exception_text = (
                    "Expected {argument} to be of {type_}, not {actual}"
                )
                for i, (argument, type_) in enumerate(hints_args.items()):
                    if type_ is not None and not isinstance(args[i], type_):
                        raise ValidationError(
                            exception_text.format(
                                argument=argument,
                                type_=type_,
                                actual=type(args[i]),
                            )
                        )
                for argument, type_ in hints_kwargs.items():
                    if not isinstance(kwargs[argument], type_):
                        raise ValidationError(
                            exception_text.format(
                                argument=argument,
                                type_=type_,
                                actual=type(kwargs[argument]),
                            )
                        )
                return_ = method(*args, **kwargs)
                if hints_return is not None and not isinstance(
                    return_, hints_return
                ):
                    raise ValidationError(
                        exception_text.format(
                            argument="return",
                            type_=hints_return,
                            actual=type(return_),
                        )
                    )
                return return_

            return decorated

        # decorate the functions of the engine
        engine = wrapper._engine
        for engine_method in (
            "run",
            "add_atom",
            "delete_atom",
            "update_position",
            "update_velocity",
            "get_velocity",
            "get_position",
        ):
            setattr(
                engine,
                engine_method,
                verify_hints(getattr(engine, engine_method)),
            )

        return wrapper
