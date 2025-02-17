"use client"

import { TrendingUp } from "lucide-react"
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts"
import { useEffect, useState } from "react";
import Papa from "papaparse";

import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
} from "@/components/ui/chart"

type SentimentData = {
    publishedAt: string,
    sentiment_label: string
};

type ProcessedData = {
    publishedAt: string;
    sentimentScore: number;
};

const chartConfig = {
    sentiment: {
        label: "Sentiment Score",
        color: "hsl(var(--chart-1))",
    },
} satisfies ChartConfig

export function SentimentChart() {
    const [data, setData] = useState<ProcessedData[]>([]);

    useEffect(() => {
        fetch("/data/sentiment_analysis_results.csv")
            .then((res) => res.text())
            .then((csvData) => {
                const parsed = Papa.parse<SentimentData>(csvData, {
                    header: true,
                    skipEmptyLines: true,
                });

                if (parsed.data && Array.isArray(parsed.data)) {
                    const sentimentMap: Record<string, { sum: number; count: number }> = {};

                    parsed.data.forEach((row) => {
                        const date = row.publishedAt.split(" ")[0];
                        const sentimentScore =
                            row.sentiment_label === "Positive" ? 1 :
                                row.sentiment_label === "Neutral" ? 0 :
                                    row.sentiment_label === "Negative" ? -1 : 0;

                        if (!sentimentMap[date]) {
                            sentimentMap[date] = { sum: 0, count: 0 };
                        }
                        sentimentMap[date].sum += sentimentScore;
                        sentimentMap[date].count += 1;
                    });

                    const aggregatedData = Object.entries(sentimentMap).map(([date, { sum, count }]) => ({
                        publishedAt: date,
                        sentimentScore: sum / count, // Average sentiment score
                    }));

                    setData(aggregatedData);
                }
            })
            .catch((error) => console.error("Error parsing CSV:", error));
    }, []);

    return (
        <Card className="m-10 w-1/2">
            <CardHeader>
                <CardTitle className="text-green-500 text-3xl">NVIDIA</CardTitle>
                <CardDescription>Showing the sentiment of people</CardDescription>
            </CardHeader>
            <CardContent>
                <ChartContainer config={chartConfig} >
                    <LineChart
                        accessibilityLayer
                        data={data}
                        margin={{
                            left: 12,
                            right: 12,
                        }}
                    >
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="publishedAt"
                            tickLine={false}
                            axisLine={false}
                            tickMargin={10}
                            interval={2}

                        />
                        <YAxis
                            domain={[-1.5, 1.5]}
                        />
                        <ChartTooltip
                            cursor={false}
                            content={<ChartTooltipContent hideLabel />}
                        />
                        <Line
                            dataKey="sentimentScore"
                            type="linear"
                            stroke="green"
                            strokeWidth={2}
                            dot={false}

                        />
                    </LineChart>
                </ChartContainer>
            </CardContent>
            <CardFooter>
                <div className="flex w-full items-start gap-2 text-sm">
                    <div className="grid gap-2">
                        <div className="flex items-center gap-2 leading-none text-muted-foreground">

                        </div>
                    </div>
                </div>
            </CardFooter>
        </Card>
    );
}
