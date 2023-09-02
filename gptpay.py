import tkinter as tk
from tkinter import messagebox

# 费率
CHARGE_PER_1K_TOKENS_INPUT = 0.03  # 输入每1000token收费标准
CHARGE_PER_1K_TOKENS_OUTPUT = 0.06  # 输出每1000token收费标准
TOKENS_PER_CHARACTER = 1  # 每个汉字占2个tokens,为1时直接按token数计算
TOKENS_PER_PUNCTUATION = 1  # 每个标点符号占1个token
EXCHANGE_RATE = 7.3  # 人民币到美元的汇率

def calculate_cost(input_characters, output_characters, exchange_rate):
    # 将字符数转换为 token 数量
    input_tokens = input_characters * TOKENS_PER_CHARACTER
    output_tokens = output_characters * TOKENS_PER_CHARACTER

    # 计算费用（美元）
    input_cost_usd = (input_tokens / 1000) * CHARGE_PER_1K_TOKENS_INPUT
    output_cost_usd = (output_tokens / 1000) * CHARGE_PER_1K_TOKENS_OUTPUT

    # 总费用（美元）
    total_cost_usd = input_cost_usd + output_cost_usd

    # 转换为人民币
    input_cost_cny = input_cost_usd * exchange_rate
    output_cost_cny = output_cost_usd * exchange_rate
    total_cost_cny = total_cost_usd * exchange_rate

    return (input_cost_usd, output_cost_usd, total_cost_usd,
            input_cost_cny, output_cost_cny, total_cost_cny)

def calculate():
    global TOKENS_PER_CHARACTER
    try:
        input_chars = int(input_entry.get())
        output_chars = int(output_entry.get())
        exchange_rate = float(rate_entry.get())
        if chinese_var.get() == 1:
            TOKENS_PER_CHARACTER = 2
        else:
            TOKENS_PER_CHARACTER = 1
        results = calculate_cost(input_chars, output_chars, exchange_rate)
        
        result_text.set(f"提问成本: ${results[0]:.2f} (¥{results[3]:.2f})\n"
                        f"回答成本: ${results[1]:.2f} (¥{results[4]:.2f})\n"
                        f"总成本: ${results[2]:.2f} (¥{results[5]:.2f})")
    except ValueError:
        messagebox.showerror("非法输入", "请确保提问和回答字符框及汇率框中填入有效数字。")

root = tk.Tk()
root.title("ChatGPT API费用计算器")

description_label = tk.Label(root, text="此计算程序为粗算，主要用于ChatGPT 4.0 API的费用计算。")
description_label.grid(row=0, column=0, columnspan=4, padx=10, pady=20)

input_label = tk.Label(root, text="提问字符数:")
input_label.grid(row=1, column=0, padx=10, pady=10)

input_entry = tk.Entry(root)
input_entry.grid(row=1, column=1, padx=10, pady=10)

output_label = tk.Label(root, text="回答字符数:")
output_label.grid(row=1, column=2, padx=10, pady=10)

output_entry = tk.Entry(root)
output_entry.grid(row=1, column=3, padx=10, pady=10)

chinese_var = tk.IntVar()
chinese_check = tk.Checkbutton(root, text="计算汉字(每个汉字占2个tokens)", variable=chinese_var)
chinese_check.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

rate_label = tk.Label(root, text="汇率(默认7.3):")
rate_label.grid(row=2, column=2, padx=10, pady=10)

rate_entry = tk.Entry(root)
rate_entry.grid(row=2, column=3, padx=10, pady=10)
rate_entry.insert(0, '7.3')

calculate_button = tk.Button(root, text="计算费用", command=calculate)
calculate_button.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text)
result_label.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()
