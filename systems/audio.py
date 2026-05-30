# ============================================================================
# NOUTRORA RPG — SISTEMA DE ÁUDIO
# ============================================================================
# Gerencia música de fundo, efeitos sonoros de inimigos e transições.
# ============================================================================

import os
from pathlib import Path

# Tenta importar pygame
try:
    import pygame
    _PYGAME_DISPONIVEL = True
except ImportError:
    _PYGAME_DISPONIVEL = False


# ============================================================================
# CAMINHO BASE DE ÁUDIO
# ============================================================================

AUDIO_BASE = Path(__file__).parent.parent / "musicas"
SOUNDTRACKS_PATH = AUDIO_BASE / "soundtracks"
CREATURES_PATH = AUDIO_BASE / "criaturas"


# ============================================================================
# INICIALIZAR PYGAME MIXER
# ============================================================================

def _inicializar_mixer():
    """Tenta inicializar pygame mixer. Retorna True se sucesso."""
    if not _PYGAME_DISPONIVEL:
        return False
    try:
        pygame.mixer.init()
        return True
    except Exception as e:
        return False


# ============================================================================
# GERENCIADOR GLOBAL DE ÁUDIO
# ============================================================================

class AudioManager:
    """
    Gerencia reprodução de música e efeitos sonoros.
    Singleton com cache de sons para otimização.
    """
    
    _instancia = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia
    
    def __init__(self):
        if getattr(self, '_inicializado', False):
            return
        
        self._inicializado = True
        self._mixer_ok = _inicializar_mixer()
        self.musica_ativa = None
        self.volume_musica = 0.7
        self.volume_sfx = 0.8
        self._cache_sons = {}  # Cache de sons carregados
        self.sons_inimigos = {}
        self._carregar_mapeamento_sons()
    
    def _carregar_mapeamento_sons(self):
        """Mapeia cada tipo de inimigo para seus sons."""
        self.sons_inimigos = {
            "Goblin": {
                "aparecimento": CREATURES_PATH / "goblin" / "goblin_snarl.wav",
                "acerto": CREATURES_PATH / "goblin" / "goblin_hit.wav",
                "morte": CREATURES_PATH / "goblin" / "goblin_death.wav",
            },
            "Goblin Mutante": {
                "aparecimento": CREATURES_PATH / "mut_goblin" / "mgoblin_btSTART.wav",
                "acerto": CREATURES_PATH / "mut_goblin" / "mgoblin_hit.wav",
                "morte": CREATURES_PATH / "mut_goblin" / "mgoblin_death.wav",
            },
            "Sombra Errante": {
                "aparecimento": CREATURES_PATH / "shadow" / "shadow_btSTART.wav",
                "acerto": CREATURES_PATH / "shadow" / "shadow_hit.wav",
                "morte": CREATURES_PATH / "shadow" / "shadow_death.wav",
            },
            "Esqueleto Guardiao": {
                "aparecimento": CREATURES_PATH / "skeleton" / "creature-skeleton-bones-hit-02.wav",
                "acerto": CREATURES_PATH / "skeleton" / "creature-skeleton-bones-hit-02.wav",
                "morte": CREATURES_PATH / "skeleton" / "creature-skeleton-death-bones-shatter-02.wav",
            },
            "Amalgama de Carne": {
                "aparecimento": CREATURES_PATH / "skeleton" / "creature-skeleton-bones-hit-02.wav",
                "acerto": CREATURES_PATH / "skeleton" / "creature-skeleton-bones-hit-02.wav",
                "morte": CREATURES_PATH / "skeleton" / "creature-skeleton-death-bones-shatter-02.wav",
            },
            "Entidade Antica": {
                "aparecimento": CREATURES_PATH / "shadow" / "shadow_btSTART.wav",
                "acerto": CREATURES_PATH / "shadow" / "shadow_hit.wav",
                "morte": CREATURES_PATH / "shadow" / "shadow_death.wav",
            },
        }
    
    def disponivel(self):
        """Retorna True se áudio está disponível e funcional."""
        return self._mixer_ok
    
    def _arquivo_existe(self, caminho):
        """Verifica se arquivo existe."""
        try:
            return Path(caminho).exists()
        except:
            return False
    
    def _obter_som_cache(self, caminho):
        """Obtém som do cache ou carrega novo."""
        caminho_str = str(caminho)
        
        if caminho_str not in self._cache_sons:
            if not self._arquivo_existe(caminho_str):
                return None
            try:
                som = pygame.mixer.Sound(caminho_str)
                self._cache_sons[caminho_str] = som
            except Exception:
                return None
        
        return self._cache_sons.get(caminho_str)
    
    def tocar_musica_principal(self):
        """Toca MAIN.wav em loop (continua tocando se já está ativa)."""
        if not self._mixer_ok:
            return
        
        # Se já está tocando MAIN, não fazer nada
        if self.musica_ativa == "main":
            try:
                if pygame.mixer.music.get_busy():
                    return
            except Exception:
                pass
        
        caminho = SOUNDTRACKS_PATH / "MAIN.wav"
        if not self._arquivo_existe(caminho):
            return
        
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(str(caminho))
            pygame.mixer.music.set_volume(self.volume_musica)
            pygame.mixer.music.play(-1)  # -1 = loop infinito
            self.musica_ativa = "main"
        except Exception:
            self._mixer_ok = False
    
    def tocar_musica_batalha(self):
        """Toca BATTLE.wav durante combate (continua tocando se já está ativa)."""
        if not self._mixer_ok:
            return
        
        # Se já está tocando BATTLE, não fazer nada
        if self.musica_ativa == "battle":
            try:
                if pygame.mixer.music.get_busy():
                    return
            except Exception:
                pass
        
        caminho = SOUNDTRACKS_PATH / "BATTLE.wav"
        if not self._arquivo_existe(caminho):
            return
        
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(str(caminho))
            pygame.mixer.music.set_volume(self.volume_musica)
            pygame.mixer.music.play(-1)  # -1 = loop infinito
            self.musica_ativa = "battle"
        except Exception:
            self._mixer_ok = False
    
    def pausar_musica(self):
        """Pausa a música atual."""
        if not self._mixer_ok:
            return
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass
    
    def resumir_musica(self):
        """Retoma a música pausada."""
        if not self._mixer_ok:
            return
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass
    
    def parar_musica(self):
        """Para a reprodução de música."""
        if not self._mixer_ok:
            return
        try:
            pygame.mixer.music.stop()
            self.musica_ativa = None
        except Exception:
            pass
    
    def tocar_som_inimigo(self, tipo_inimigo, evento="acerto"):
        """
        Toca som de um inimigo específico.
        
        Args:
            tipo_inimigo: tipo do inimigo (ex: "Goblin")
            evento: "aparecimento", "acerto" ou "morte"
        """
        if not self._mixer_ok:
            return
        
        if tipo_inimigo not in self.sons_inimigos:
            return
        
        sons = self.sons_inimigos[tipo_inimigo]
        if evento not in sons:
            return
        
        caminho = sons[evento]
        som = self._obter_som_cache(caminho)
        
        if som:
            try:
                som.set_volume(self.volume_sfx)
                som.play()
            except Exception:
                pass
    
    def definir_volume_musica(self, volume):
        """Define volume da música (0.0 a 1.0)."""
        self.volume_musica = max(0.0, min(1.0, float(volume)))
        if not self._mixer_ok:
            return
        try:
            pygame.mixer.music.set_volume(self.volume_musica)
        except Exception:
            pass
    
    def definir_volume_sfx(self, volume):
        """Define volume dos efeitos sonoros (0.0 a 1.0)."""
        self.volume_sfx = max(0.0, min(1.0, float(volume)))
    
    def limpar_cache(self):
        """Limpa cache de sons carregados."""
        self._cache_sons.clear()


# Instância global
audio_manager = AudioManager()
