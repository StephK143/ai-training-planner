import React, { useState } from "react";
import {
  Button,
  TextField,
  Card,
  CardContent,
  Typography,
  CircularProgress,
} from "@mui/material";

interface CareerPath {
  description: string;
  courses: Array<{
    id: string;
    name: string;
    requiredOrder: number;
  }>;
  badges: Array<{
    id: string;
    name: string;
    requiredOrder: number;
  }>;
  estimatedTime: string;
  milestones: string[];
}

interface Props {
  userData: any; // Replace with proper user data type
  onPathSelect: (path: CareerPath) => void;
}

export const CareerAdvisor: React.FC<Props> = ({ userData, onPathSelect }) => {
  const [preferences, setPreferences] = useState("");
  const [loading, setLoading] = useState(false);
  const [careerPaths, setCareerPaths] = useState<CareerPath[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [selectedPath, setSelectedPath] = useState<CareerPath | null>(null);
  const [feedback, setFeedback] = useState("");

  const getCareerPaths = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/career/paths", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_data: userData,
          career_preferences: preferences,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch career paths");
      }

      const data = await response.json();
      setCareerPaths(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const refinePath = async () => {
    if (!selectedPath) return;

    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/career/refine", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_data: userData,
          selected_path: selectedPath,
          user_feedback: feedback,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to refine career path");
      }

      const data = await response.json();
      // Update the selected path with refined data
      setSelectedPath(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Typography variant="h5" gutterBottom sx={{ color: "#e3f2fd" }}>
        Career Path Advisor
      </Typography>

      <TextField
        fullWidth
        multiline
        rows={4}
        variant="outlined"
        label="Career Preferences"
        placeholder="Describe your career goals and preferences..."
        value={preferences}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
          setPreferences(e.target.value)
        }
        margin="normal"
        sx={{
          "& .MuiOutlinedInput-root": {
            "& fieldset": {
              borderColor: "#4f5b62",
            },
            "&:hover fieldset": {
              borderColor: "#90caf9",
            },
            "&.Mui-focused fieldset": {
              borderColor: "#90caf9",
            },
          },
          "& .MuiInputLabel-root": {
            color: "#90caf9",
          },
          "& .MuiOutlinedInput-input": {
            color: "#e3f2fd",
          },
          "& .MuiInputLabel-root.Mui-focused": {
            color: "#90caf9",
          },
        }}
      />

      <Button
        variant="contained"
        color="primary"
        onClick={getCareerPaths}
        disabled={loading || !preferences}
        sx={{
          mt: 2,
          mb: 4,
          backgroundColor: "#1976d2",
          "&:hover": {
            backgroundColor: "#2196f3",
          },
          "&.Mui-disabled": {
            backgroundColor: "#1e293b",
            color: "#90a4ae",
          },
        }}
      >
        {loading ? <CircularProgress size={24} /> : "Get Career Paths"}
      </Button>

      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}

      {careerPaths.map((path, index) => (
        <Card
          key={index}
          sx={{
            mb: 2,
            cursor: "pointer",
            backgroundColor: "#1e1e2f",
            border:
              selectedPath === path ? "2px solid #90caf9" : "1px solid #4f5b62",
            "&:hover": {
              borderColor: "#90caf9",
              boxShadow: "0 0 10px rgba(144, 202, 249, 0.2)",
            },
          }}
          onClick={() => setSelectedPath(path)}
        >
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ color: "#e3f2fd" }}>
              Career Path {index + 1}
            </Typography>
            <Typography variant="body1" sx={{ color: "#e3f2fd" }}>
              {path.description}
            </Typography>

            <Typography variant="subtitle1" sx={{ mt: 2, color: "#90caf9" }}>
              Required Courses:
            </Typography>
            <ul style={{ color: "#e3f2fd" }}>
              {path.courses.map((course) => (
                <li key={course.id}>{course.name}</li>
              ))}
            </ul>

            <Typography variant="subtitle1" sx={{ color: "#90caf9" }}>
              Required Badges:
            </Typography>
            <ul style={{ color: "#e3f2fd" }}>
              {path.badges.map((badge) => (
                <li key={badge.id}>{badge.name}</li>
              ))}
            </ul>

            <Typography variant="body2" sx={{ color: "#90caf9" }}>
              Estimated Time:{" "}
              <span style={{ color: "#e3f2fd" }}>{path.estimatedTime}</span>
            </Typography>

            <Typography variant="subtitle1" sx={{ mt: 2, color: "#90caf9" }}>
              Key Milestones:
            </Typography>
            <ul style={{ color: "#e3f2fd" }}>
              {path.milestones.map((milestone, i) => (
                <li key={i}>{milestone}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      ))}

      {selectedPath && (
        <>
          <TextField
            fullWidth
            multiline
            rows={3}
            variant="outlined"
            label="Questions or Feedback"
            placeholder="Ask questions or provide feedback about this career path..."
            value={feedback}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setFeedback(e.target.value)
            }
            margin="normal"
            sx={{
              "& .MuiOutlinedInput-root": {
                "& fieldset": {
                  borderColor: "#4f5b62",
                },
                "&:hover fieldset": {
                  borderColor: "#90caf9",
                },
                "&.Mui-focused fieldset": {
                  borderColor: "#90caf9",
                },
              },
              "& .MuiInputLabel-root": {
                color: "#90caf9",
              },
              "& .MuiOutlinedInput-input": {
                color: "#e3f2fd",
              },
              "& .MuiInputLabel-root.Mui-focused": {
                color: "#90caf9",
              },
            }}
          />

          <Button
            variant="contained"
            color="secondary"
            onClick={refinePath}
            disabled={loading || !feedback}
            sx={{
              mt: 2,
              backgroundColor: "#9c27b0",
              "&:hover": {
                backgroundColor: "#ba68c8",
              },
              "&.Mui-disabled": {
                backgroundColor: "#1e293b",
                color: "#90a4ae",
              },
            }}
          >
            {loading ? <CircularProgress size={24} /> : "Refine Path"}
          </Button>

          <Button
            variant="contained"
            color="primary"
            onClick={() => onPathSelect(selectedPath)}
            sx={{
              mt: 2,
              ml: 2,
              backgroundColor: "#1976d2",
              "&:hover": {
                backgroundColor: "#2196f3",
              },
            }}
          >
            Select This Path
          </Button>
        </>
      )}
    </div>
  );
};
