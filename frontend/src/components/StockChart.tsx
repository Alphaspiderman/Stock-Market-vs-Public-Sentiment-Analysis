"use client";

import { TrendingUp } from "lucide-react";
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts";
import { useEffect, useState } from "react";
import Papa from "papaparse";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

// CSV format: Date,Open,High,Low,Close,Volume,Dividends,Stock Splits,Ticker
type CSVData = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  dividends: number;
  stockSplits: number;
  ticker: string;
};

type ProcessedData = {
  date: string;
  stockPrice: number;
};

const chartConfig = {
  sentiment: {
    label: "Sentiment Score",
    color: "hsl(var(--chart-1))",
  },
} satisfies ChartConfig;

export function StockChart() {
  const [data, setData] = useState<ProcessedData[]>([]);

  useEffect(() => {
    fetch("/data/stock_data.csv")
      .then((res) => res.text())
      .then((csvData) => {
        const parsed = Papa.parse<CSVData>(csvData, {
          header: true,
          skipEmptyLines: true,
        });

        if (parsed.data && Array.isArray(parsed.data)) {

          const aggregatedData = parsed.data.map((row) => ({
            date: row.date.split(" ")[0],
            stockPrice: row.close,
          }));

          setData(aggregatedData);
        }
      })
      .catch((error) => console.error("Error parsing CSV:", error));
  }, []);

  return (
    <Card className="m-10 w-3/4">
      <CardHeader>
        <CardTitle className="text-green-500 text-3xl">NVIDIA</CardTitle>
        <CardDescription>Showing the stock prices</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
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
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={10}
              interval={5}
            />
            <YAxis domain={[100, 475]} />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Line
              dataKey="stockPrice"
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
            <div className="flex items-center gap-2 leading-none text-muted-foreground"></div>
          </div>
        </div>
      </CardFooter>
    </Card>
  );
}
