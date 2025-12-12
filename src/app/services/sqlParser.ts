// Dummy SQL Parser Service
// TODO: Replace with actual API call to backend later
// Example API call: POST /api/parse-nl-to-sql { naturalLanguage: string } -> { sql: string }

interface ParseResponse {
  sql: string;
  explanation: string;
}

const dummySqlExamples: Record<string, string> = {
  age_platform_hours: "SELECT * FROM users WHERE age > 50 AND platform = 'youtube' AND daily_hours > 15;",
  age_only: "SELECT * FROM users WHERE age > 50;",
  platform_hours: "SELECT * FROM users WHERE platform = 'youtube' AND daily_hours > 15;",
  all_users: "SELECT * FROM users;",
  age_income: "SELECT * FROM users WHERE age > 30 AND income > 50000;",
  location_age: "SELECT * FROM users WHERE location = 'New York' AND age < 40;",
  purchase_count: "SELECT user_id, COUNT(*) as purchase_count FROM purchases GROUP BY user_id HAVING COUNT(*) > 5;",
  average_spend: "SELECT AVG(amount) as average_spending FROM orders WHERE date > '2024-01-01';",
};

export function generateDummySqlResponse(naturalLanguage: string): ParseResponse {
  // Simple keyword matching to generate dummy SQL
  const input = naturalLanguage.toLowerCase().trim();

  // Check if input is too vague/short to parse
  const validKeywords = [
    "age", "platform", "hour", "income", "location", "purchase", 
    "count", "average", "spend", "date", "user", "select", "where",
    // Location aliases
    "york", "city", "town", "country", "state", "region","Vietnam",
    // Age aliases
    "year", "old", "above", "below", "over", "under",   
    
    // Platform aliases
    "youtube", "facebook", "twitter", "instagram", "tiktok",
    // Time/Hour aliases
    "hours", "daily", "watch", "use", "spend"
  ];
  
  const hasValidKeywords = validKeywords.some(keyword => input.includes(keyword));
  
  // If input is too short or has no relevant keywords, ask for more details
  if (input.length < 3 || !hasValidKeywords) {
    return {
      sql: "",
      explanation: "Sorry, I need more detail information please. Please provide a query like: 'Find users older than 50 who use YouTube more than 15 hours daily'",
    };
  }

  let selectedExample = dummySqlExamples.all_users;
  let explanation = "Query to retrieve all users";

  // Detect location-related keywords
  const hasLocation = input.includes("location") || input.includes("york") || input.includes("city") || input.includes("town") || input.includes("country") || input.includes("state") || input.includes("region");
  const hasAge = input.includes("age") || input.includes("year") || input.includes("old");
  const hasPlatform = input.includes("platform") || input.includes("youtube") || input.includes("facebook") || input.includes("twitter") || input.includes("instagram") || input.includes("tiktok");
  const hasHours = input.includes("hour") || input.includes("daily") || input.includes("watch") || input.includes("spend");
  const hasIncome = input.includes("income") || input.includes("earning") || input.includes("salary");
  const hasCount = input.includes("count") || input.includes("number");
  const hasAverage = input.includes("average") || input.includes("avg");

  if (hasAge && hasPlatform && hasHours) {
    selectedExample = dummySqlExamples.age_platform_hours;
    explanation = "Query to find users above certain age using specific platform for specified hours";
  } else if (hasAge && hasIncome) {
    selectedExample = dummySqlExamples.age_income;
    explanation = "Query to find users by age and income range";
  } else if (hasLocation && hasAge) {
    selectedExample = dummySqlExamples.location_age;
    explanation = "Query to find users by location and age";
  } else if (hasCount && input.includes("purchase")) {
    selectedExample = dummySqlExamples.purchase_count;
    explanation = "Query to count purchases per user";
  } else if (hasAverage && input.includes("spend")) {
    selectedExample = dummySqlExamples.average_spend;
    explanation = "Query to calculate average spending";
  } else if (hasAge) {
    selectedExample = dummySqlExamples.age_only;
    explanation = "Query to filter users by age";
  } else if (hasPlatform && hasHours) {
    selectedExample = dummySqlExamples.platform_hours;
    explanation = "Query to find users by platform and usage hours";
  }

  return {
    sql: selectedExample,
    explanation,
  };
}

// Simulated API call - replace with actual backend call later
export async function parseNaturalLanguageToSQL(
  naturalLanguage: string
): Promise<ParseResponse> {
  // Simulate network delay
  await new Promise((resolve) => setTimeout(resolve, 800));

  // TODO: Replace with actual API call:
  // const response = await fetch('/api/parse-nl-to-sql', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ naturalLanguage })
  // });
  // return response.json();

  return generateDummySqlResponse(naturalLanguage);
}
