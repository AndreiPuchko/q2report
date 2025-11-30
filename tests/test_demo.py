import importlib
import pkgutil
import pathlib


def get_test_set():
    for folder in os.listdir(test_data_folder):
        test_input_docx_filename = f"{test_data_folder}/{folder}/test.docx"
        test_input_xlsx_filename = f"{test_data_folder}/{folder}/test.xlsx"
        test_result_file_name = f"test-result/test-result_{folder}.docx"
        yield test_input_docx_filename, test_input_xlsx_filename, test_result_file_name


def t_est_merge():
    for test_input_docx_filename, test_input_xlsx_filename, test_result_file_name in get_test_set():
        result = q2data2docx.merge(test_input_docx_filename, test_input_xlsx_filename, test_result_file_name)
        assert result is True


def run_demos_test(format="docx"):
    demo_pkg = "demo"
    demo_path = pathlib.Path(__file__).parent.parent / demo_pkg

    for module_info in pkgutil.iter_modules([str(demo_path)]):
        name = module_info.name
        if name.startswith("demo_"):
            module_name = f"{demo_pkg}.{name}"

            print(f"▶ Running {module_name}.demo('{format}')")

            # Импортируем модуль
            mod = importlib.import_module(module_name)

            # Вызываем функцию demo(), если есть
            func = getattr(mod, "demo", None)
            if callable(func):
                func(format)
            else:
                print(f"⚠ {module_name} does not have a demo() function")


def test_demos_docx():
    run_demos_test("docx")


def test_demos_xlsx():
    run_demos_test("xlsx")


def test_demos_pdf():
    run_demos_test("pdf")


def test_demos_html():
    run_demos_test("html")

if __name__ == "__main__":
    test_demos_docx()