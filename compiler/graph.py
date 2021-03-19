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
    if block.flow_to:
      self.render_blk(block.flow_to)
      self.add_edge(block, block.flow_to)
    else:
      for blk in InterRepr.blks:
        if block.flows_to(blk):
          block.flow_to = blk
          self.render_blk(blk)
          self.add_edge(block, blk)
    if block.branch_to:
      self.render_blk(block.branch_to)
      self.add_edge(block, block.branch_to, branch=True)
    # for blk in InterRepr.blks:
    #   self.add_block(blk)
    #   for blk2 in InterRepr.blks:
    #     if blk.flows_to(blk2):
    #       self.add_edge(blk, blk2)
    #     if blk.branches_to(blk2):
    #       self.add_edge(blk,blk2, branch=True)

  def add_block(self, block: BasicBlock):
    instructions = self.add_instructions(block.instructions)
    self.s.node(f"BB{block.idx}",
                f"BB{block.idx} | {instructions}")

  def add_edge(self, src: BasicBlock, dest: BasicBlock, branch=False):
    label = "branch" if branch else "flow-through"
    self.s.edge(f'BB{src.idx}:s', f'BB{dest.idx}:n', label=label)

  def add_instructions(self, instructions: List[Instruction]):
    return f"{{{'|'.join(map(str, instructions))} }}"