import { useState, useEffect, useRef } from "react";
import { Inria_Sans } from "next/font/google";
import { IconBot, IconMan, IconLoading, IconAddActive, IconAddInactive, IconMicOn, IconMicOff, IconSendOn, IconSendOff } from "./Icons";

const inriaSans = Inria_Sans({ 
  subsets: ["latin"], 
  weight: ["300", "400", "700"],
  variable: '--font-inria' 
});

export const ChatConversation = ({ messages, isLoading }: { messages: any[]; isLoading: boolean }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const shouldAutoScrollRef = useRef(true);

  // Track if user is scrolled to bottom
  const handleScroll = () => {
    if (!containerRef.current) return;
    
    const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
    const isNearBottom = scrollHeight - scrollTop - clientHeight < 100; // 100px threshold
    shouldAutoScrollRef.current = isNearBottom;
  };

  // Auto scroll only if user is near bottom
  useEffect(() => {
    if (!shouldAutoScrollRef.current || !containerRef.current) return;
    
    const container = containerRef.current;
    container.scrollTop = container.scrollHeight;
  }, [messages, isLoading]);

  return (
    <div 
      ref={containerRef}
      onScroll={handleScroll}
      className="flex-1 overflow-y-auto pb-[30px] pt-[30px] px-[30px] flex flex-col gap-6 scrollbar-hide"
      style={{
        scrollbarWidth: 'none',
        msOverflowStyle: 'none',
      }}
    >
      <style>{`
        .scrollbar-hide::-webkit-scrollbar {
          display: none;
        }
      `}</style>
      {messages.map((msg, idx) => (
        <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
          {msg.role === "bot" && <div className="w-12 h-12 shrink-0 mr-2"><IconBot /></div>}
          
          {msg.type === "sql" ? (
            <div className="max-w-[600px] p-4 rounded-tr-3xl rounded-br-3xl rounded-bl-[24px] rounded-tl-none bg-white text-black">
              <div className="text-sm text-gray-600 mb-2">{msg.explanation}</div>
              {msg.text && (
                <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto font-mono text-gray-800">
                  <code>{msg.text}</code>
                </pre>
              )}
            </div>
          ) : (
            <div className={`max-w-[400px] p-[16px] ${
              msg.role === "user" 
                ? "bg-white text-black rounded-tl-[24px] rounded-br-[24px] rounded-bl-[24px] rounded-tr-none" 
                : "bg-white text-black rounded-tr-[24px] rounded-br-[24px] rounded-bl-[24px] rounded-tl-none"
            } ${inriaSans.className} text-[15px] break-words whitespace-pre-wrap`}>
              {msg.text}
            </div>
          )}

          {msg.role === "user" && <div className="w-[50px] h-[42px] shrink-0 ml-[8px]"><IconMan /></div>}
        </div>
      ))}

      {isLoading && (
        <div className="flex justify-start">
          <div className="w-[48px] h-[48px] shrink-0 mr-[8px]"><IconBot /></div>
          <div className="bg-[#515151] p-[16px] rounded-2xl flex items-center gap-2">
            <IconLoading />
            <span className="text-white text-sm">Generating SQL...</span>
          </div>
        </div>
      )}
    </div>
  );
};

export const ChatInputArea = ({ onSendMessage }: { onSendMessage: (text: string) => void }) => {
  const [inputValue, setInputValue] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const [isAddActive, setIsAddActive] = useState(false);
  const [isMicHovered, setIsMicHovered] = useState(false);
  const [isSendHovered, setIsSendHovered] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
    
    // Auto-grow textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + "px";
    }
  };

  const handleSend = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue("");
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  return (
    <div className="w-full px-[30px] pb-[50px] flex justify-center">
      <div className="w-full max-w-[864px]">
        <div 
          className={`flex w-full min-h-[112px] p-[24px] items-end gap-[24px] rounded-[16px] transition-all duration-300
            ${isFocused 
              ? "border border-white shadow-[0_0_7px_1px_#FFF] bg-[#D9D9D9]" 
              : "border border-black bg-[#D9D9D9]"
            }`}
        >
          {/* ADD BUTTON */}
          <div 
            className="shrink-0 cursor-pointer flex justify-center items-center transition-all duration-300"
            onMouseEnter={() => setIsAddActive(true)}
            onMouseLeave={() => setIsAddActive(false)}
          >
            {isAddActive ? <IconAddActive /> : <IconAddInactive />}
          </div>

          {/* TEXTAREA FIELD */}
          <textarea 
            ref={textareaRef}
            placeholder="Type a message..." 
            className="flex-1 bg-transparent outline-none text-black px-4 font-sans text-left resize-none overflow-hidden break-words"
            style={{ minHeight: "40px", maxHeight: "200px", height: "40px" }}
            value={inputValue}
            onChange={handleInputChange}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />

          {/* MIC / SEND BUTTON */}
          <div className="shrink-0 cursor-pointer flex justify-center items-center">
            {inputValue.trim() === "" ? (
              <div 
                onMouseEnter={() => setIsMicHovered(true)}
                onMouseLeave={() => setIsMicHovered(false)}
              >
                {isMicHovered ? <IconMicOn /> : <IconMicOff />}
              </div>
            ) : (
              <div 
                onMouseEnter={() => setIsSendHovered(true)}
                onMouseLeave={() => setIsSendHovered(false)}
                onClick={handleSend}
              >
                {isSendHovered ? <IconSendOn /> : <IconSendOff />}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
