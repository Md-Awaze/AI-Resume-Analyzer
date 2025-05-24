import React from "react";

interface SkillTagProps {
	skill: string;
}

const SkillTag: React.FC<SkillTagProps> = ({ skill }) => {
	return (
		<span className="inline-block bg-blue-500 text-white px-4 py-2 rounded-full text-sm font-medium transition-transform hover:scale-105">
			{skill}
		</span>
	);
};

interface SkillsSectionProps {
	skills: string[];
}

const SkillsSection: React.FC<SkillsSectionProps> = ({ skills }) => {
	return (
		<div className="bg-white rounded-lg shadow p-6 mb-6">
			<h3 className="text-xl font-semibold text-blue-500 mb-4">
				Detected Skills
			</h3>
			<div className="flex flex-wrap gap-3">
				{skills.map((skill, index) => (
					<SkillTag key={index} skill={skill} />
				))}
			</div>
		</div>
	);
};

export default SkillsSection;
