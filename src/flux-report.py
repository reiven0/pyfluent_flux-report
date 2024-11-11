import os
import pandas as pd
from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class FluxReportConfig:
    """Configuration class for flux report"""
    definition: str
    boundaries: List[str]
    filename: str = 'output.csv'


class FluxReporter:
    """Class to manage flux report generation and storage"""

    def __init__(self, solver, config: FluxReportConfig):
        self.solver = solver
        self.config = config
        self._result: List[Dict[str, Any]] = []

    def generate_report(self) -> List[Dict[str, Any]]:
        """Generate flux report"""
        try:
            self.solver.solution.report_definitions.flux[self.config.definition] = {
            }
            mass_flow_rate = self.solver.solution.report_definitions.flux[self.config.definition]
            mass_flow_rate.boundaries.allowed_values()
            mass_flow_rate.boundaries = self.config.boundaries
            mass_flow_rate.per_zone = True

            self._result = self.solver.solution.report_definitions.compute(
                report_defs=[self.config.definition]
            )
            return self._result
        except Exception as e:
            raise FluxReportError(f"Failed to generate flux report: {str(e)}")


class ResultManager:
    """Class responsible for saving and managing results"""

    def __init__(self):
        self.base_path = self._get_base_path()
        self.result_folder = self._create_result_folder()
        self.dp_number = self._get_dp_number()

    def _get_base_path(self) -> Path:
        """Get base path for operations"""
        return Path(os.getcwd())

    def _create_result_folder(self) -> Path:
        """Create folder for storing results"""
        result_folder = self.base_path.parent.parent.parent / "result_folder"
        result_folder.mkdir(exist_ok=True)
        return result_folder

    def _get_dp_number(self) -> str:
        """Get DP number from parent directory name"""
        return self.base_path.parent.parent.name

    def save_to_csv(self, data: List[Dict], filename: str) -> None:
        """Save results to CSV file"""
        try:
            df = pd.DataFrame(data)
            # Extract first element from each column
            for column in df.columns:
                df[column] = df[column].apply(lambda x: x[0])

            # Sort columns
            df = df[sorted(df.columns)]

            # Add DP number to filename
            full_filename = self.result_folder / f"{self.dp_number}_{filename}"
            print(f"Saving to: {full_filename}")
            df.to_csv(full_filename, index=False)
        except Exception as e:
            raise ResultSaveError(f"Failed to save results: {str(e)}")


class FluxReportError(Exception):
    """Custom exception for flux report generation errors"""
    pass


class ResultSaveError(Exception):
    """Custom exception for result saving errors"""
    pass


def main(solver) -> None:
    """Main execution function"""
    try:
        # Initialize configuration
        config = FluxReportConfig(
            definition="mass_flow_rate",
            boundaries=["cha", "chb", "chc", "chd"],
            filename="output.csv"
        )

        # Generate report
        reporter = FluxReporter(solver, config)
        result = reporter.generate_report()

        # Save results
        result_manager = ResultManager()
        result_manager.save_to_csv(result, config.filename)

    except (FluxReportError, ResultSaveError) as e:
        print(f"Error: {str(e)}")
        raise


if __name__ == "MainConsole":
    # Execute when solver object is available
    main(solver)
