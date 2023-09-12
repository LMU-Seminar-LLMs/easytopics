type DefaultParagraphProps = {
  text: string;
};

const DefaultParagraph = ({ text }: DefaultParagraphProps) => (
  <p className='text-base/7'>{text}</p>
);

export default DefaultParagraph;
