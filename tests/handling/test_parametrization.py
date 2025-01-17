import asyncio

from mock import Mock

import kopf
from kopf._cogs.structs.ephemera import Memo
from kopf._core.engines.indexing import OperatorIndexers
from kopf._core.reactor.inventory import ResourceMemories
from kopf._core.reactor.processing import process_resource_event


async def test_parameter_is_passed_when_specified(resource, cause_mock, registry, settings):
    mock = Mock()

    # If it works for this handler, we assume it works for all of them.
    # Otherwise, it is too difficult to trigger the actual invocation.
    @kopf.on.event(*resource, param=123)
    def fn(**kwargs):
        mock(**kwargs)

    event_queue = asyncio.Queue()
    await process_resource_event(
        lifecycle=kopf.lifecycles.all_at_once,
        registry=registry,
        settings=settings,
        resource=resource,
        indexers=OperatorIndexers(),
        memories=ResourceMemories(),
        memobase=Memo(),
        raw_event={'type': None, 'object': {}},
        event_queue=event_queue,
    )

    assert mock.called
    assert mock.call_args_list[0][1]['param'] == 123


async def test_parameter_is_passed_even_if_not_specified(resource, cause_mock, registry, settings):
    mock = Mock()

    # If it works for this handler, we assume it works for all of them.
    # Otherwise, it is too difficult to trigger the actual invocation.
    @kopf.on.event(*resource)
    def fn(**kwargs):
        mock(**kwargs)

    event_queue = asyncio.Queue()
    await process_resource_event(
        lifecycle=kopf.lifecycles.all_at_once,
        registry=registry,
        settings=settings,
        resource=resource,
        indexers=OperatorIndexers(),
        memories=ResourceMemories(),
        memobase=Memo(),
        raw_event={'type': None, 'object': {}},
        event_queue=event_queue,
    )

    assert mock.called
    assert mock.call_args_list[0][1]['param'] is None
