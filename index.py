#! python3
#encoding: utf-8
# -*- coding: utf-8 -*-


def run_proc():
    import package_tool.grammar
    tempgrammar_var = package_tool.grammar.grammar_class()
    ttt = tempgrammar_var.method_out_put("script\\dict.txt","script\\abc.txt")
    print(ttt['str'])
    print(ttt['index'])

if __name__=='__main__':
	run_proc()