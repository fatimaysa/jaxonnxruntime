# Copyright 2023 The Jaxonnxruntime Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Define ONNX Cos operator."""
# pylint: disable=unused-argument
# pylint: disable=g-explicit-length-test
from collections.abc import Callable, Sequence
import functools
import inspect
from typing import Any

from jax import jit
from jax import numpy as jnp
from jaxonnxruntime.core import handler
from jaxonnxruntime.core import onnx_node


@handler.register_op("Cos")
class Cos(handler.Handler):
  """Implementation of the ONNX Cos operator."""

  @classmethod
  def _prepare(
      cls, node: onnx_node.OnnxNode, inputs: Sequence[Any], onnx_jax_impl: Any
  ):
    sig = inspect.signature(onnx_jax_impl)
    kwparams = [
        param.name
        for param in sig.parameters.values()
        if param.kind == inspect.Parameter.KEYWORD_ONLY
    ]
    for name in kwparams:
      node.attrs_dict[name] = node.attrs.get(name, None)

  @classmethod
  def version_7(
      cls, node: onnx_node.OnnxNode, inputs: Sequence[Any]
  ) -> Callable[..., Any]:
    """ONNX version_7 Cos op."""
    cls._prepare(node, inputs, onnx_cos)
    return onnx_cos


@functools.partial(jit, static_argnames=())
def onnx_cos(*input_args):
  """https://github.com/onnx/onnx/blob/v1.12.0/docs/Operators.md#Cos for more details."""
  assert len(input_args) == 1
  data = input_args[0]
  return jnp.cos(data)