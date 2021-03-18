from dataclasses import dataclass
from typing import List

from graphviz import Digraph

from compiler.ir.inter_repr import InterRepr
from compiler.ir.basic_block import BasicBlock
from compiler.ir.instruction import Instruction
from compiler.opcode import SSAOpCode



@dataclass
class Graph:
  filename: str = "out"
  seen: set = None

  def render(self):
    self.s = Digraph('Control Flow Graph',
      filename=f"{self.filename}.gv",
      node_attr={'shape': 'record'})

    self.seen = set()
    self.render_blk(InterRepr.root_block)

    self.s.view()

  def render_blk(self, block: BasicBlock):
    if block.idx in self.seen:
      return
    self.seen.add(block.idx)
    self.add_block(block)
    for child in block.children:
      self.render_blk(child)
      self.add_edge(block, child)

  def add_block(self, block: BasicBlock):
    instructions = self.add_instructions(block.instructions)
    self.s.node(f"BB{block.idx}",
                f"BB{block.idx} | {instructions}")

  def add_edge(self, src: BasicBlock, dest: BasicBlock):
    is_branch = src.exit_point.branches_to(dest.entry_point)
    label = "Branch" if is_branch else "Flow-through"
    self.s.edge(f'BB{src.idx}:s', f'BB{dest.idx}:n', label=label)

  def add_instructions(self, instructions: List[Instruction]):
    return f"{{{'|'.join(map(str, instructions))} }}"