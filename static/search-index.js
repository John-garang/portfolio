// Comprehensive search index for all pages
const searchIndex = [
    { 
        title: 'Home', 
        url: 'index.html', 
        content: 'john garang digital communications portfolio skills graphic design web development social media management email marketing seo search engine optimization content creation visual storytelling project management ghost writing copywriting microsoft office digital strategy photography cinematography brand identity html5 facebook newsletters keywords planning how i work with clients welcome to my digital garden south sudanese professional strategic communications expert content creator digital marketing specialist brand storyteller'
    },
    { 
        title: 'About Me', 
        url: 'about.html', 
        content: 'john ngor deng garang south sudanese leader communicator designer storytelling engagement social impact african leadership university entrepreneurial leadership bachelor degree education talent opportunity career communication strategy partnerships projects content pieces social media growth online presence learning experiences coordinated projects meaningful partnerships communication engagement understanding people bridging gaps messages resonate unleash global innovation lab young african leaders initiative yali un conference youth climate change take action lab jim leech mastercard foundation entrepreneurship leadership relationships trust lasting impact resilience skill opportunity global stage communications professional contact email mobile whatsapp kampala uganda nickname ghost high school favorite pastime traveling reading books wildlife photography restaurants board games graduated university life self-development bachelor hons entrepreneurial leadership april 2026 favorite animal lions majesty strength courage justice military might king of beasts awe-inspiring strength dominance la popa monastery cartagena colombia best college memory house party best advice guilt past baggage holding back soaring high new day fight hard fight clean run fast long life never look back nobody knows heart better trust instincts shadow sunshine conversation starters television shows vampire diaries originals lucifer fast furious avatar beers country songs travel culture community hiking design'
    },
    { 
        title: 'Work Portfolio', 
        url: 'work-portfolio.html', 
        content: 'work portfolio projects experience professional work collection showcase career achievements accomplishments'
    },
    { 
        title: 'My Shelf', 
        url: 'my-shelf.html', 
        content: 'my shelf writings articles publications medium blog posts thought leadership content writing personal essays stories narratives perspectives insights reflections'
    },
    { 
        title: 'Artefacts', 
        url: 'artefacts.html', 
        content: 'artefacts creative projects portfolio little bet innovations project tshinsha amakahya national indaba creative connect social media africa inventor alliance linkedin profile personal writings creative work design projects innovation initiatives community engagement'
    },
    { 
        title: 'CV / Resume', 
        url: 'cv.html', 
        content: 'cv curriculum vitae resume professional experience education skills qualifications work history career timeline achievements certifications training'
    },
    { 
        title: 'Graphic Design', 
        url: 'graphic-design.html', 
        content: 'graphic design visual design branding creative work logo design brand identity visual communication design portfolio creative projects illustrations typography color theory layout design print design digital design'
    },
    { 
        title: 'Experience Overview', 
        url: 'experience-overview.html', 
        content: 'experience overview work history career professional experience 4 years blending corporate non-profit work digital communications education organizations companies roles responsibilities achievements'
    },
    { 
        title: 'African Leadership University', 
        url: 'african-leadership-university.html', 
        content: 'african leadership university alu education entrepreneurial leadership bachelor degree mauritius rwanda student experience campus life learning community innovation entrepreneurship africa leadership development skills training academic programs'
    },
    { 
        title: 'Education Bridge', 
        url: 'education-bridge.html', 
        content: 'education bridge teaching learning educational organization tutoring mentoring students academic support learning programs educational initiatives community education'
    },
    { 
        title: 'African Leadership Academy', 
        url: 'african-leadership-academy.html', 
        content: 'african leadership academy ala south africa johannesburg high school education leadership training young african leaders entrepreneurship innovation community service'
    },
    { 
        title: 'Ashinaga Foundation', 
        url: 'ashinaga-foundation.html', 
        content: 'ashinaga foundation scholarship financial support education orphans students africa japan international scholarship program educational opportunity'
    },
    { 
        title: 'Uganics Repellents Ltd', 
        url: 'uganics-repellents.html', 
        content: 'uganics repellents ltd uganda business mosquito repellent natural products health wellness malaria prevention entrepreneurship startup company'
    },
    { 
        title: 'Africa Inventor Alliance', 
        url: 'africa-inventor-alliance.html', 
        content: 'africa inventor alliance innovation inventors creativity problem solving african innovations technology solutions entrepreneurship innovation ecosystem community support'
    },
    { 
        title: 'Surplus People Project', 
        url: 'surplus-people-project.html', 
        content: 'surplus people project south africa land rights community development social justice advocacy ngo non-profit organization rural communities'
    },
    { 
        title: 'Creative Connect', 
        url: 'creative-connect.html', 
        content: 'creative connect social media marketing digital marketing content creation brand management online presence social media strategy facebook instagram twitter linkedin engagement community management'
    },
    { 
        title: 'Nalafem Collective', 
        url: 'nalafem-collective.html', 
        content: 'nalafem collective community organization women empowerment social impact collective action community development'
    },
    { 
        title: 'Programs Overview', 
        url: 'programs-overview.html', 
        content: 'programs overview training fellowship leadership programs professional development capacity building skills training workshops seminars conferences'
    },
    { 
        title: 'CNN Academy Fellow', 
        url: 'cnn-academy.html', 
        content: 'cnn academy fellow voices global south journalism climate storytelling july 2025 november 2025 newsroom skills immersive learning cnn correspondents multimedia reporting ethics journalism art storytelling news breaks reporting field digital storytelling writing digital social storytelling writing news live television script writing open source reporting artificial intelligence journalism ai tools techniques modern journalism peer collaboration story pitching climate stories international media global audiences network storytellers environmental change abu dhabi fellowship program climate experts media leaders professional bonds ethics journalism fundamental principles ethical reporting media responsibility art storytelling crafting compelling narratives engage inform audiences breaking news real-time reporting techniques field reporting on-location journalism skills field reporting techniques digital storytelling creating multimedia content digital platforms writing digital optimizing content online audiences platforms social storytelling leveraging social media impactful journalism writing news live television broadcast writing techniques television news script writing professional scriptwriting various media formats open source reporting utilizing open source intelligence investigative journalism artificial intelligence journalism integrating ai tools techniques modern journalism collaborative learning global network peer collaboration collaborative workshops fellows global south critiqued refined work broadening perspectives building connections story pitching sessions pitching climate stories international media learning frame narratives global audiences global network connected global network storytellers equally committed driving environmental change journalism program challenged think critically representation ensuring stories regions told accuracy dignity urgency'
    },
    { 
        title: 'Take Action Lab', 
        url: 'take-action-lab.html', 
        content: 'take action lab leadership program social entrepreneurship innovation problem solving community development action-oriented learning practical skills'
    },
    { 
        title: 'UNLEASH Innovation Lab', 
        url: 'unleash-innovation-lab.html', 
        content: 'unleash innovation lab sdg sustainable development goals sustainability innovation global challenges solutions united nations agenda 2030 innovation talent kigali rwanda december 2023 climate land track pappybags papyrus reeds plastic bags south sudan environmental pollution economic empowerment sustainable materials biodegradable reusable tote bags colombia gambia united states pakistan iceland cross-cultural collaboration rapid ideation human-centered design systems thinking impact pitching global network changemakers nonprofit accelerate progress mobilizing young changemakers immersive innovation labs regional programs co-create scalable real-world solutions mentors investors ngos governments copenhagen singapore china greenland rwanda thousands young leaders hundreds impactful sdg-focused projects'
    },
    { 
        title: 'Accra Fusion', 
        url: 'accra-fusion.html', 
        content: 'accra fusion ghana africa cultural exchange program networking collaboration african professionals diaspora community building cultural immersion'
    },
    { 
        title: 'YALI East Africa', 
        url: 'yali-east-africa.html', 
        content: 'yali young african leaders initiative east africa leadership training us state department program civic leadership business entrepreneurship public management networking'
    },
    { 
        title: 'Services', 
        url: 'services.html', 
        content: 'services professional services consulting design development graphic design web development social media management content creation digital marketing strategy branding email marketing seo optimization project management'
    },
    { 
        title: 'Contact', 
        url: 'contact.html', 
        content: 'contact get in touch email phone reach out connect communication contact information dengjohn200@gmail.com mobile whatsapp kampala uganda message inquiry collaboration opportunities'
    }
];
