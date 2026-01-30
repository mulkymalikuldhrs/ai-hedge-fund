"""Test suite for all 7 sub-agents."""

import pytest
import sqlite3
from pathlib import Path

from src.agents.base_agent import BaseAgent, PlanExecutionResult, StepResult
from src.agents.code_skeptic_agent import CodeSkepticAgent
from src.agents.checking_agent import CheckingAgent
from src.agents.production_agent import ProductionAgent
from src.agents.review_agent import ReviewAgent
from src.agents.debugging_agent import DebuggingAgent
from src.agents.refactoring_agent import RefactoringAgent
from src.agents.documentation_agent import DocumentationAgent


@pytest.fixture
def code_skeptic_agent():
    agent = CodeSkepticAgent()
    yield agent
    # Cleanup: close database connections if needed


@pytest.fixture
def checking_agent():
    agent = CheckingAgent()
    yield agent


@pytest.fixture
def production_agent():
    agent = ProductionAgent()
    yield agent


@pytest.fixture
def review_agent():
    agent = ReviewAgent()
    yield agent


@pytest.fixture
def debugging_agent():
    agent = DebuggingAgent()
    yield agent


@pytest.fixture
def refactoring_agent():
    agent = RefactoringAgent()
    yield agent


@pytest.fixture
def documentation_agent():
    agent = DocumentationAgent()
    yield agent


class TestCodeSkepticAgent:
    """Test CodeSkepticAgent (P0)."""

    def test_initialization(self, code_skeptic_agent):
        assert code_skeptic_agent.agent_name == "CodeSkepticAgent"
        assert code_skeptic_agent.db_path == "data/code_skeptic_agent.db"

    def test_phase_definition(self, code_skeptic_agent):
        assert len(code_skeptic_agent.phase_definition) == 5
        phase_names = [phase[0] for phase in code_skeptic_agent.phase_definition]
        assert "claim_verification" in phase_names
        assert "quality_gates" in phase_names

    def test_database_creation(self, code_skeptic_agent):
        assert Path(code_skeptic_agent.db_path).exists()
        conn = sqlite3.connect(code_skeptic_agent.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "claims" in tables
        assert "quality_gates" in tables
        conn.close()

    def test_execute_plan_small(self, code_skeptic_agent):
        result = code_skeptic_agent.execute_plan(max_steps=5)
        assert isinstance(result, PlanExecutionResult)
        assert result.agent_name == "CodeSkepticAgent"
        assert result.total_steps_executed == 5
        assert result.successful_steps == 5
        assert result.failed_steps == 0
        assert result.success

    def test_execute_plan_full(self, code_skeptic_agent):
        result = code_skeptic_agent.execute_plan()
        assert result.total_steps_executed == 100
        assert result.successful_steps == 100
        assert result.failed_steps == 0
        assert result.success

    def test_get_signal(self, code_skeptic_agent):
        import pandas as pd

        result = code_skeptic_agent.get_signal("AAPL", pd.DataFrame())
        assert "agent_name" in result
        assert "ticker" in result
        assert "signal" in result


class TestCheckingAgent:
    """Test CheckingAgent (P1)."""

    def test_initialization(self, checking_agent):
        assert checking_agent.agent_name == "CheckingAgent"

    def test_phase_definition(self, checking_agent):
        assert len(checking_agent.phase_definition) == 5
        phase_names = [phase[0] for phase in checking_agent.phase_definition]
        assert "system_health" in phase_names

    def test_execute_plan(self, checking_agent):
        result = checking_agent.execute_plan(max_steps=10)
        assert result.total_steps_executed == 10
        assert result.success

    def test_database_tables(self, checking_agent):
        conn = sqlite3.connect(checking_agent.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "health_checks" in tables
        assert "system_status" in tables
        conn.close()


class TestProductionAgent:
    """Test ProductionAgent (P1)."""

    def test_initialization(self, production_agent):
        assert production_agent.agent_name == "ProductionAgent"

    def test_phase_definition(self, production_agent):
        assert len(production_agent.phase_definition) == 5
        phase_names = [phase[0] for phase in production_agent.phase_definition]
        assert "production_logging" in phase_names

    def test_execute_plan(self, production_agent):
        result = production_agent.execute_plan(max_steps=10)
        assert result.total_steps_executed == 10
        assert result.success

    def test_database_tables(self, production_agent):
        conn = sqlite3.connect(production_agent.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "logs" in tables
        assert "metrics" in tables
        assert "health_checks" in tables
        conn.close()


class TestReviewAgent:
    """Test ReviewAgent (P2)."""

    def test_initialization(self, review_agent):
        assert review_agent.agent_name == "ReviewAgent"

    def test_phase_definition(self, review_agent):
        assert len(review_agent.phase_definition) == 4
        phase_names = [phase[0] for phase in review_agent.phase_definition]
        assert "code_quality_review" in phase_names
        assert "architecture_review" in phase_names

    def test_execute_plan(self, review_agent):
        result = review_agent.execute_plan(max_steps=10)
        assert result.total_steps_executed == 10
        assert result.success

    def test_database_tables(self, review_agent):
        conn = sqlite3.connect(review_agent.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "code_issues" in tables
        assert "architecture_reviews" in tables
        assert "security_reviews" in tables
        conn.close()


class TestDebuggingAgent:
    """Test DebuggingAgent (P3)."""

    def test_initialization(self, debugging_agent):
        assert debugging_agent.agent_name == "DebuggingAgent"

    def test_phase_definition(self, debugging_agent):
        assert len(debugging_agent.phase_definition) == 5
        phase_names = [phase[0] for phase in debugging_agent.phase_definition]
        assert "debug_infrastructure" in phase_names

    def test_execute_plan(self, debugging_agent):
        result = debugging_agent.execute_plan(max_steps=10)
        assert result.total_steps_executed == 10
        assert result.success

    def test_database_tables(self, debugging_agent):
        conn = sqlite3.connect(debugging_agent.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "error_reports" in tables
        assert "debug_sessions" in tables
        conn.close()


class TestRefactoringAgent:
    """Test RefactoringAgent (P4)."""

    def test_initialization(self, refactoring_agent):
        assert refactoring_agent.agent_name == "RefactoringAgent"

    def test_phase_definition(self, refactoring_agent):
        assert len(refactoring_agent.phase_definition) == 5
        phase_names = [phase[0] for phase in refactoring_agent.phase_definition]
        assert "refactoring_assessment" in phase_names

    def test_execute_plan(self, refactoring_agent):
        result = refactoring_agent.execute_plan(max_steps=10)
        assert result.total_steps_executed == 10
        assert result.success

    def test_database_tables(self, refactoring_agent):
        conn = sqlite3.connect(refactoring_agent.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "code_smells" in tables
        assert "refactoring_tasks" in tables
        conn.close()


class TestDocumentationAgent:
    """Test DocumentationAgent (P5)."""

    def test_initialization(self, documentation_agent):
        assert documentation_agent.agent_name == "DocumentationAgent"

    def test_phase_definition(self, documentation_agent):
        assert len(documentation_agent.phase_definition) == 5
        phase_names = [phase[0] for phase in documentation_agent.phase_definition]
        assert "audit_consolidation" in phase_names

    def test_execute_plan(self, documentation_agent):
        result = documentation_agent.execute_plan(max_steps=10)
        assert result.total_steps_executed == 10
        assert result.success

    def test_database_tables(self, documentation_agent):
        conn = sqlite3.connect(documentation_agent.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "documentation_reports" in tables
        assert "documentation_issues" in tables
        conn.close()


class TestAgentIntegration:
    """Test integration across all agents."""

    def test_all_agents_initializable(self):
        agents = [
            CodeSkepticAgent(),
            CheckingAgent(),
            ProductionAgent(),
            ReviewAgent(),
            DebuggingAgent(),
            RefactoringAgent(),
            DocumentationAgent(),
        ]
        assert len(agents) == 7
        for agent in agents:
            assert hasattr(agent, "phase_definition")

    def test_all_databases_created(self):
        db_paths = [
            "data/code_skeptic_agent.db",
            "data/checking_agent.db",
            "data/production_agent.db",
            "data/review_agent.db",
            "data/debugging_agent.db",
            "data/refactoring_agent.db",
            "data/documentation_agent.db",
        ]
        for db_path in db_paths:
            assert Path(db_path).exists()

    def test_all_agents_execute_100_steps(self):
        agents = [
            CodeSkepticAgent(),
            CheckingAgent(),
            ProductionAgent(),
            ReviewAgent(),
            DebuggingAgent(),
            RefactoringAgent(),
            DocumentationAgent(),
        ]
        for agent in agents:
            result = agent.execute_plan()
            assert result.total_steps_executed == 100
            assert result.success

    def test_total_steps_count(self):
        agents = [
            CodeSkepticAgent(),
            CheckingAgent(),
            ProductionAgent(),
            ReviewAgent(),
            DebuggingAgent(),
            RefactoringAgent(),
            DocumentationAgent(),
        ]
        total_steps = sum(
            len(phase[2]) for agent in agents for phase in agent.phase_definition
        )
        assert total_steps == 700
