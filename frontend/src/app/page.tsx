import { SentimentChart } from "@/components/SentimentChart";
import { StockChart } from "@/components/StockChart";

export default function Home() {
  return (
    <div className="flex flex-col justify-center items-center p-4">
      <h1 className="text-center text-5xl mt-10 font-bold">Analysis of Public Sentiment on NVIDIA</h1>
      <SentimentChart />
      <StockChart />
    </div>
  );
}
