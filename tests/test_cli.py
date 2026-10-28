import argparse
import pytest

from cli import build_parser

def test_add_parses_description_and_amount():
    parser = build_parser()
    args = parser.parse_args(["add", "--description", "Lunch", "--amount", "20"])
    assert args.command == "add"
    assert args.description == "Lunch"
    assert args.amount == 20.0
    assert args.category == "Uncategorized"


def test_add_parses_category_when_provided():
    parser = build_parser()
    args = parser.parse_args(
        ["add", "--description", "Pizza", "--amount", "12", "--category", "Food"]
    )
    assert args.category == "Food"


def test_list_with_no_flags():
    parser = build_parser()
    args = parser.parse_args(["list"])
    assert args.command == "list"
    assert args.category is None


def test_list_with_category_filter():
    parser = build_parser()
    args = parser.parse_args(["list", "--category", "Food"])
    assert args.category == "Food"


def test_summary_month_is_parsed_as_int():
    parser = build_parser()
    args = parser.parse_args(["summary", "--month", "9"])
    assert args.month == 9


def test_add_rejects_negative_amount():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["add", "--description", "X", "--amount", "-5"])


def test_add_rejects_non_numeric_amount():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["add", "--description", "X", "--amount", "abc"])


def test_add_rejects_missing_description():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["add", "--amount", "20"])


def test_summary_rejects_month_above_12():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["summary", "--month", "13"])


def test_summary_rejects_month_below_1():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["summary", "--month", "0"])


def test_summary_accepts_all_valid_months():
    parser = build_parser()
    for m in range(1, 13):
        args = parser.parse_args(["summary", "--month", str(m)])
        assert args.month == m


def test_unknown_command_rejected():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["notacommand"])


def test_no_commad_rejected():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_end_to_end_add_and_list(temp_storage, monkeypatch, capsys):
    import sys
    from cli import main

    # Simulate: python main.py add --description "Coffee" --amount 4
    monkeypatch.setattr(sys, "argv", ["main.py", "add", "--description", "Coffee", "--amount", "4"])
    main()

    captured = capsys.readouterr()
    assert "Expense added successfully" in captured.out

    # Simulate: python main.py list
    monkeypatch.setattr(sys, "argv", ["main.py", "list"])
    main()

    captured = capsys.readouterr()
    assert "Coffee" in captured.out

