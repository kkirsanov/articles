.globl factorial
  factorial:
          movl      $1, %eax
          jmp      .L2
  .L3:
          imull     4(%esp), %eax
          decl      4(%esp)
  .L2:
          cmpl      $1, 4(%esp)
          jg       .L3
          ret
