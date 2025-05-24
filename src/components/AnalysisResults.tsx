import React from "react";
import NotificationBanner from "./NotificationBanner";
import SkillsSection from "./SkillsSection";
import SuggestionsSection from "./SuggestionsSection";
import MatchScoreSection from "./MatchScoreSection";

interface AnalysisResultsProps {
	results: {
		skills: string[];
		suggestions: string[];
		matchScore: number;
		status: string;
	} | null;
	showNotification: boolean;
	onHideNotification: () => void;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({
	results,
	showNotification,
	onHideNotification,
}) => {
	if (!results) return null;

	return (
		<div className="space-y-6">
			<NotificationBanner
				message={results.status}
				type="success"
				show={showNotification}
				onHide={onHideNotification}
			/>

			{/* Results Container */}
			<div className="bg-white rounded-xl shadow-sm p-8">
				<h2 className="text-2xl font-bold text-gray-900 mb-6">
					Resume Analysis Results
				</h2>

				{/* Skills Section */}
				<SkillsSection skills={results.skills} />

				{/* Suggestions Section */}
				<SuggestionsSection suggestions={results.suggestions} />

				{/* Match Score Section */}
				<MatchScoreSection score={results.matchScore} />
			</div>
		</div>
	);
};

export default AnalysisResults;
