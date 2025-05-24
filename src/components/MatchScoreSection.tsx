import React, { useEffect, useRef } from "react";

interface MatchScoreSectionProps {
	score: number;
}

const MatchScoreSection: React.FC<MatchScoreSectionProps> = ({ score }) => {
	const circleRef = useRef<HTMLDivElement>(null);

	useEffect(() => {
		if (circleRef.current) {
			// Ensure score is between 0 and 100
			const clampedScore = Math.min(Math.max(score, 0), 100);

			// Update the circular progress
			circleRef.current.style.background = `conic-gradient(rgb(59, 130, 246) ${
				clampedScore * 3.6
			}deg, #eee ${clampedScore * 3.6}deg)`;

			// Add animation class
			circleRef.current.classList.add("animate-pulse");

			// Remove animation class after animation completes
			const timer = setTimeout(() => {
				if (circleRef.current) {
					circleRef.current.classList.remove("animate-pulse");
				}
			}, 300);

			return () => clearTimeout(timer);
		}
	}, [score]);

	return (
		<div className="bg-white rounded-lg shadow p-6 mb-6">
			<h3 className="text-xl font-semibold text-blue-500 mb-4">
				Job Match Score
			</h3>
			<div className="flex justify-center items-center p-5">
				<div
					ref={circleRef}
					className="relative w-36 h-36 rounded-full flex items-center justify-center"
				>
					<div className="absolute w-32 h-32 rounded-full bg-white" />
					<div className="relative z-10 flex items-baseline">
						<span className="text-4xl font-bold text-blue-500">
							{Math.round(score)}
						</span>
						<span className="text-2xl text-blue-500 ml-1">%</span>
					</div>
				</div>
			</div>
		</div>
	);
};

export default MatchScoreSection;
