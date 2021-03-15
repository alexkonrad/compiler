from dataclasses import dataclass
from typing import List

from graphviz import Digraph

from compiler.ir.inter_repr import InterRepr
from compiler.ir.basic_block import BasicBlock
from compiler.ir.instruction import Instruction



@dataclass
class Graph:
  filename: str = "out"
  num_nodes: int = 0

  def render(self):
    self.s = Digraph('Control Flow Graph',
      filename=f"{self.filename}.gv",
      node_attr={'shape': 'record'})

    for block in InterRepr.blks:
      self.add_block(block)

    for block in InterRepr.blks:
      for child in block.children:
        self.add_edge(block, child)

    self.s.view()

  def add_block(self, block: BasicBlock):
    self.num_nodes += 1

    instructions = self.add_instructions(block.instructions)
    self.s.node(f"BB{block.idx}",
                f"BB{block.idx} | {instructions}")

  def add_edge(self, src: BasicBlock, dest: BasicBlock):
    self.s.edge(f'BB{src.idx}', f'BB{dest.idx}')

  def add_instructions(self, instructions: List[Instruction]):
    return f"{{{'|'.join(map(str, instructions))} }}"