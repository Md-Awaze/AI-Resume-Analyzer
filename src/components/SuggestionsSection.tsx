import React from "react";

interface SuggestionsSectionProps {
	suggestions: string[];
}

const SuggestionsSection: React.FC<SuggestionsSectionProps> = ({
	suggestions,
}) => {
	return (
		<div className="bg-white rounded-lg shadow p-6 mb-6">
			<h3 className="text-xl font-semibold text-blue-500 mb-4">
				Improvement Suggestions
			</h3>
			<ul className="space-y-3">
				{suggestions.map((suggestion, index) => (
					<li
						key={index}
						className="py-3 border-b last:border-b-0 text-gray-700 hover:text-gray-900 transition-colors"
					>
						{suggestion}
					</li>
				))}
			</ul>
		</div>
	);
};

export default SuggestionsSection;
